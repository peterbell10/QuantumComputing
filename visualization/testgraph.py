def plots():
    global vlgaBuffSorted
    cntr()

    result = collections.defaultdict(list)
    for d in vlgaBuffSorted:
        result[d['event']].append(d)

    result_list = result.values()

    f = Figure()
    graph1 = f.add_subplot(211)
    graph2 = f.add_subplot(212,sharex=graph1)

    for item in result_list:
        tL = []
        vgsL = []
        vdsL = []
        isubL = []
        for dict in item:
            tL.append(dict['time'])
            vgsL.append(dict['vgs'])
            vdsL.append(dict['vds'])
            isubL.append(dict['isub'])
        graph1.plot(tL,vdsL,'bo',label='a')
        graph1.plot(tL,vgsL,'rp',label='b')
        graph2.plot(tL,isubL,'b-',label='c')

    plotCanvas = FigureCanvasTkAgg(f, pltFrame)
    toolbar = NavigationToolbar2TkAgg(plotCanvas, pltFrame)
    toolbar.pack(side=BOTTOM)
    plotCanvas.get_tk_widget().pack(side=TOP)


