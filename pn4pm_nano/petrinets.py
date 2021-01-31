#### Definition of some repeatable functions used from the objects ####
def check_gateways(check_gtw, all_gtws):
    found = 0
    for gtws in all_gtws:
        if check_gtw[2:4] == gtws[2:4]:
            found = 1
    return found


def iterable(obj):
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return True


class Petrinet:
    temp = []
    idx = 0

    def __init__(self, labels, places=[], transitions=[], edges=[], inc_gateways=None, exc_gateways=None,
                 parall_gateways=None):
        self.labels = labels
        self.places = places
        self.transitions = transitions
        self.names_transitions = []
        self.start_end_transition = []
        self.start_end_places = []
        self.edges = edges
        self.inc_gateways = inc_gateways
        self.exc_gateways = exc_gateways
        self.parall_gateways = parall_gateways
        self.all_gateways = []
        self.new_labels = []
        self.del_sil_act()
        self.reduce_duplicates()
        self.create_start_end_events()
        self.create_nf()
        self.create_gateways()
        self.create_transitions()
        self.create_places()

    def reduce_duplicates(self):
        # find all duplicates in the list and delete them and reconnect it
        for label in self.labels:
            if label[0] != "":
                for duplicate in self.labels:
                    if label[0] == duplicate[0] and label[1] != duplicate[1]:
                            # replace the connection by the original
                            if iterable(duplicate[2]):
                                for dup in duplicate[2]:
                                    if iterable(label[2]):
                                        if dup not in label[2]: label[2].append(dup)
                                    elif label[2] != dup:
                                        label[2] = [label[2], dup]
                            else:
                                if iterable(label[2]):
                                    if duplicate[2] not in label[2]: label[2].append(duplicate[2])
                                elif label[2] != duplicate[2]:
                                    label[2] = [label[2], duplicate[2]]
                            # now search for all activities which show to the duplicate
                            for resource in self.labels:
                                if iterable(resource[2]):
                                    # append the vg information to the original
                                    if duplicate[1] in resource[2]:
                                        for it, res in enumerate(resource[2]):
                                            if res == duplicate[1]: resource[2][it] = label[1]
                                elif duplicate[1] == resource[2]:
                                    resource[2] = label[1]
                            # drop the duplicate from the lists
                            self.labels.remove(duplicate)
        raenge = []
        for label in self.labels:
            raenge.append(label[1])
        for label in self.labels:
            if iterable(label[2]):
                label[2] = [x for x in label[2] if x in raenge]
                label[2] = list(dict.fromkeys(label[2]))
                if label[1] == min([row[1] for row in self.labels]):
                    label[2].append(min([row[1] for row in self.labels]) - 1)
            else:
                if label[1] == min([row[1] for row in self.labels]):
                    label[2] = min([row[1] for row in self.labels]) - 1

    def del_sil_act(self):
        stopper = False
        while not stopper:
            for label in self.labels:
                # silent activity
                if label[0] == "":
                    # go to the following activities
                    for fa in self.labels:
                        # connect the previous activity to all following activities
                        if iterable(fa[2]):
                            if label[1] in fa[2]:
                                if iterable(label[2]):
                                    fa[2].extend(label[2])
                                    fa[2] = list(dict.fromkeys(fa[2]))
                                else:
                                    fa[2].append(label[2])
                        elif label[1] == fa[2]:
                            fa[2] = label[2]
                    # last activity with ""?
                    if len([x for x in self.labels if x[0] == ""]) <= 1: stopper = True
                    # delete item
                    self.labels.remove(label)
                    # break to restart
                    break
        raenge = []
        for label in self.labels:
            raenge.append(label[1])
        for label in self.labels:
            if iterable(label[2]):
                label[2] = [x for x in label[2] if x in raenge]
            if label[1] == min([row[1] for row in self.labels]):
                label[2] = min([row[1] for row in self.labels]) - 1


    def create_nf(self):
        # find all following activities to each activity
        for label in self.labels:
            nf = []
            for row in self.labels:
                if iterable(row[2]):
                    if label[1] in row[2]:
                        nf.append(row[1])
                else:
                    if label[1] == row[2]:
                        nf.append(row[1])

            label.append(nf)
            label.append(-1)
            if label[0] in ['Start_Event', 'End_Event']:
                label.append(-2)
            else:
                label.append(-1)

    def create_start_end_events(self):
        # start event
        mini = min([row[1] for row in self.labels])
        maxi = max([row[1] for row in self.labels])
        self.labels.append(['Start_Event', mini - 1, mini - 2])
        self.labels.append(['End_Event', maxi + 1, maxi])

    def create_gateways(self):
        self.new_labels = self.labels
        ocount = 0
        # run all activities
        for act in self.new_labels:
            if iterable(act[3]):
                # if its an activity with multiple following activities create a fork gateway
                if len(act[3]) > 1 and '_gtw_' not in act[0]:
                    ocount += 1
                    gtwid = max([row[1] for row in self.labels]) + 1
                    gateway = [f'fork_gtw_{ocount}', gtwid, act[1], act[3], 0, -1]
                    self.new_labels.append(gateway)
                    act[3] = gtwid
                    # reconnect the old connections
                    for rep in self.new_labels:
                        if iterable(rep[2]):
                            if act[1] in rep[2] and 'fork_gtw_' not in rep[0]:
                                rep[2] = [gtwid if x == act[1] else x for x in rep[2]]

                        else:
                            if act[1] == rep[2] and 'fork_gtw_' not in rep[0]:
                                rep[2] = gtwid
        # run all activities again
        ocount = 0
        for act in self.new_labels:
            if iterable(act[2]):
                if len(act[2]) > 1:
                    for a in act[2]:
                        ocount += 1
                        gtwid = max([row[1] for row in self.labels]) + 1
                        gateway = [f'merge_gtw_{ocount}', gtwid, a, act[1], 1, -1]
                        self.new_labels.append(gateway)
                        for rep in self.new_labels:
                            if rep[1] == a:
                                rep[3] = [gtwid if x == act[1] else x for x in rep[3]]
                        act[2] = [gtwid if x == gateway[2] else x for x in act[2]]

    def create_transitions(self):
        # creating the transition list
        self.transitions = []
        for c, label in enumerate(self.new_labels):
            self.transitions.append(f"T_{c}")
            if label[5] == -1 and label[4] == -1 and label[0] != "":
                self.names_transitions.append([label[0], f"T_{c}"])
            if label[5] == -2:
                self.start_end_transition.append(f"T_{c}")
            label.append(f"T_{c}")

    def create_places(self):
        temp = []
        a = 0
        for key, rf, vg, nf, type, art, label in self.new_labels:
            # merged points
                if iterable(vg):
                    a += 1
                    for fo in vg:
                        for key2, rf2, vg2, nf2, type2, art2, label2 in self.new_labels:
                            if fo == rf2:
                                temp.append([label, label2, f"P_{a}"])
                                break
                            if rf == min([row[1] for row in self.new_labels]):
                                a += 1
                                temp.append([label, 'NONE', f"P_{a}"])
                                break
                else:
                    for key2, rf2, vg2, nf2, type2, art2, label2 in self.new_labels:
                        if vg == rf2:
                            a += 1
                            temp.append([label, label2, f"P_{a}"])
                            break
                        if rf == min([row[1] for row in self.new_labels]):
                            a += 1
                            temp.append([label, 'NONE', f"P_{a}"])
                            break
        places = []
        edges = []
        for c, b, place in temp:
            places.append(place)
            if b != 'NONE' and [b, place] not in edges:
                edges.append([b, place])
            if  [place, c] not in edges:
                edges.append([place, c])
        edges.append([self.start_end_transition[1], f"P_{a + 1}"])
        places.append(f"P_{a + 1}")
        # drop duplicates
        places = list(set(places))
        self.places = places
        self.edges = edges
        starter = []
        ender = []
        for edge in edges:
            if self.start_end_transition[0] == edge[1]:
                starter = edge[0]
            if self.start_end_transition[1] == edge[0]:
                ender = edge[1]
        self.start_end_places = [starter, ender]

    def output(self, tablename=None):
        if tablename == None:
            tablename = "ActivityTable"
        string = f"({tablename},{self.places},{self.transitions},{self.edges},{self.start_end_places},{self.names_transitions})"
        return string

    def cel_out(self,tablename=None):
        if tablename is None:
            tablename = "ActivityTable"
        place = '''["''' + '''" "'''.join(self.places) + '''"]'''
        transition = '''["''' + '''" "'''.join(self.transitions) + '''"]'''
        s_e = '''["''' + '''"], ["'''.join(self.start_end_places) + '''"]'''
        newarc = '''['''
        for arclist in self.edges:
            arc = '''["''' + '''" "'''.join(arclist) + '''"]'''
            newarc = newarc + arc
        newarc = newarc + ''']'''
        newlabel = '''['''
        for t in self.names_transitions:
            label = '''[\'''' + '''' \"'''.join(t) + '''"]'''
            newlabel = newlabel + label
        newlabel = newlabel + ''']'''

        string = f'''CONFORMANCE({tablename}, {place}, {transition}, {newarc}, {newlabel}, {s_e} )'''
        return string

    def pmpy_out(self):
        return "Output Dummy"
