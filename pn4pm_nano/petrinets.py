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
        self.create_start_end_events()
        self.create_nf()
        self.create_gateways()
        self.integrate_gateways()
        self.create_transitions()
        self.create_places()

    def create_nf(self):
        # find all following activities to each activity
        for label in self.labels:
            nf = []
            for row in self.labels:
                try:
                    for vg in row[2]:
                        if label[1] == vg:
                            nf.append(row[1])
                except:
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
        # checks if gateways are given. If not search for gatesways and create inclusive gateways for them
        if self.exc_gateways is not None:
            self.exc_gateways[:] = [tup for tup in self.exc_gateways if not check_gateways(tup, self.all_gateways)]
            for gtw in self.exc_gateways:
                gtw.append(len(self.all_gateways))
                gtw.append(0)
                self.all_gateways.append(gtw)
        if self.parall_gateways is not None:
            self.parall_gateways[:] = [tup for tup in self.parall_gateways if not check_gateways(tup,
                                                                                                 self.all_gateways)]
            for gtw in self.parall_gateways:
                gtw.append(len(self.all_gateways))
                gtw.append(1)
                self.all_gateways.append(gtw)
        if self.inc_gateways is not None:
            self.inc_gateways[:] = [tup for tup in self.inc_gateways if not check_gateways(tup, self.all_gateways)]
            for gtw in self.inc_gateways:
                gtw.append(len(self.all_gateways))
                gtw.append(2)
                self.all_gateways.append(gtw)
        # check the labels if there are any undefined gateways found and make inc gateways out of it
        for label in self.labels:
            found = 0
            for tup in self.all_gateways:
                if label[1] in tup[2:4]:
                    found = 1
                    break
            if found == 0 and (iterable(label[2]) or len(label[3]) > 1):
                # check if an gateway
                gtw = []
                if iterable(label[2]):
                    gtw = [f"inc_gateway_close_{len(self.all_gateways)}", 1, label[2], label[1]]
                if len(label[3]) > 1:
                    gtw = [f"inc_gateway_open_{len(self.all_gateways)}", 0, label[1], label[3]]
                gtw.append(len(self.all_gateways))
                gtw.append(2)
                self.all_gateways.append(gtw)

    def integrate_gateways(self):
        # put activities and gateways together
        self.new_labels = self.labels
        starting_list = [e[2] for e in self.all_gateways if e[1] == 0]
        ending_list = [e[3] for e in self.all_gateways if e[1] == 1]
        counter = len(self.new_labels)
        it = 0
        for label in self.new_labels:
            it += 1
            if it > counter: break
            if label[1] in starting_list:
                gname, gtype, gbefore, gafter, gid, gart = [e for e in self.all_gateways if e[2] == label[1]][0]
                label[3] = [len(self.new_labels) + 1]
                # add the opener gateway
                self.new_labels.append([gname, label[3][0], gbefore, gafter, gtype, gart])
                for l in gafter:
                    for a in self.new_labels:
                        if a[1] == l:
                            a[2] = label[3][0]
                            break
            if label[1] in ending_list:
                # add closing gateways
                gname, gtype, gbefore, gafter, gid, gart = [e for e in self.all_gateways if e[3] == label[1]][0]
                label[2] = len(self.new_labels) + 1
                # add the closing gateway
                self.new_labels.append([gname, label[2], gbefore, gafter, gtype, gart])
                for l in gbefore:
                    for a in self.new_labels:
                        if a[1] == l:
                            a[3] = [label[2]]
                            break

    def create_transitions(self):
        # creating the transition list
        self.transitions = []
        for c, label in enumerate(self.new_labels):
            self.transitions.append(f"T_{c}")
            if label[5] == -1 and label[0] != "":
                self.names_transitions.append([label[0], f"T_{c}"])
            if label[5] == -2:
                self.start_end_transition.append(f"T_{c}")
            label.append(f"T_{c}")

    def create_places(self):
        temp = []
        a = 0

        for key, rf, vg, nf, type, art, label in self.new_labels:
                if iterable(vg):
                    for fo in vg:
                        for key2, rf2, vg2, nf2, type2, art2, label2 in self.new_labels:
                            if fo == rf2:
                                a += 1
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
            if b != 'NONE':
                edges.append([b, place])
            edges.append([place, c])
        edges.append([self.start_end_transition[1], f"P_{a + 1}"])
        places.append(f"P_{a + 1}")
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

