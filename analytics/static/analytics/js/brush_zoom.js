/** 
 * Copyright 2016, 2017 UFPE - Universidade Federal de Pernambuco
 * 
 * Este arquivo é parte do programa Amadeus Sistema de Gestão de Aprendizagem, ou simplesmente Amadeus LMS
 * 
 * O Amadeus LMS é um software livre; você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU como publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença.
 * 
 * Este programa é distribuído na esperança que possa ser útil, mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
 * 
 * Você deve ter recebido uma cópia da Licença Pública Geral GNU, sob o título "LICENSE", junto com este programa, se não, escreva para a Fundação do Software Livre (FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.
*/


var ganttCont = 0;
var temp, temp2;
class GanttChart {
    constructor(chartConfig) {
        this.create(GanttChart.validData(chartConfig));
    }
    static validData(chartConfig) {
        if (chartConfig.data == undefined) {
            console.error("Without Dataset");
            throw new Exeption();
        }
        chartConfig.sugest = {
            width: 1200,
            height: 300,
            windowProp: 5 / 2,
            chartProp: 12 / 3,
        };
        if (chartConfig.name == undefined) chartConfig.name = "GanttChart" + (ganttCont++);
        if (chartConfig.parent == undefined) chartConfig.parent = "body";

        if (chartConfig.parents == undefined) chartConfig.parents = {};
        if (chartConfig.parents.focus == undefined) chartConfig.parents.focus = chartConfig.parent;
        if (chartConfig.parents.context == undefined) chartConfig.parents.context = chartConfig.parents.focus;
        if (chartConfig.parents.legend == undefined) chartConfig.parents.legend = chartConfig.parent;

        if (chartConfig.dimensions == undefined) chartConfig.dimensions = {};

        if (chartConfig.margin == undefined) chartConfig.margin = {};
        if (chartConfig.margin.top == undefined) chartConfig.margin.top = 20;
        if (chartConfig.margin.right == undefined) chartConfig.margin.right = 10;
        if (chartConfig.margin.bottom == undefined) chartConfig.margin.bottom = 25;
        if (chartConfig.margin.left == undefined) chartConfig.margin.left = 10;

        if (chartConfig.layout == undefined) chartConfig.layout = {};
        if (chartConfig.layout.maxrow == undefined) chartConfig.layout.maxrow = 5;
        if (chartConfig.layout.contextHeight == undefined) chartConfig.layout.contextHeight = 0.15;
        if (chartConfig.layout.colors == undefined)
            chartConfig.layout.colors = ["#AD1111", "#FAA916", "#0B4F6C", "#343434", "#00993F"]
        if (chartConfig.layout.texts == undefined || chartConfig.layout.texts.length != chartConfig.layout.colors.length)
            chartConfig.layout.texts = ["Atrasada", "Dentro do Prazo", "Pendência Futura", "Perdida", "Concluída"];
        if (chartConfig.layout.texts2 == undefined || chartConfig.layout.texts2.length != chartConfig.layout.colors.length)
            chartConfig.layout.texts2 = ["Esta tarefa está atrasada", "Você ainda não realizou esta tarefa", "", "Você perdeu esta tarefa", ""];
        if (chartConfig.layout.min_size_card == undefined) chartConfig.layout.min_size_card = 200;
        if (chartConfig.layout.backcolor == undefined) chartConfig.layout.backcolor = "#F5F5F5";
        if (chartConfig.layout.percent_min == undefined) chartConfig.layout.percent_min = 0.3;
        if (chartConfig.layout.percent_text == undefined) chartConfig.layout.percent_text = "Tarefa já realizada por % dos participantes";
        if (chartConfig.layout.buttonAccess_text == undefined) chartConfig.layout.buttonAccess_text = "ACESSAR TAREFA";
        if (chartConfig.layout.buttonDoTask_text == undefined) chartConfig.layout.buttonDoTask_text = "REALIZAR TAREFA";
        if (chartConfig.layout.initDate_text == undefined) chartConfig.layout.initDate_text = "Data/Hora inicial: ";
        if (chartConfig.layout.endDate_text == undefined) chartConfig.layout.endDate_text = "Data/Hora final: ";
        if (chartConfig.layout.closedDate_text == undefined) chartConfig.layout.closedDate_text = "Tarefa encerrada em: ";

        chartConfig.now = new Date();
        var now = chartConfig.now.getTime();

        var positions = [];
        for (var i = 0; i < chartConfig.layout.maxrow; i++)
            positions.push(null);

        function type(d, i) {
            //Validação linha a linha
            if (d == undefined)
                return
            if (d.date == undefined ||
                d.date.start == undefined ||
                d.date.end == undefined ||
                d.name == undefined) {
                console.error("invalid row of dataSet \"" + i + "\" ");
                throw new Exception();
            }
            if (d.percent == undefined) d.percent = 0;
            d.percent = +d.percent;
            if (d.percent > 1) d.percent = 1;
            if (d.percent < 0) d.percent = 0;
            //Configurando datas
            if (d.date.start != undefined && d.date.start != "") {
                d.date.start = new Date(d.date.start);
            }

            if (d.date.end != undefined && d.date.end != "") {
                d.date.end = new Date(d.date.end);
            }

            if (d.date.delay != undefined && d.date.delay != "") {
                d.date.delay = new Date(d.date.delay);
            } else {
                d.date.delay = d.date.end;
            }

            /*if (d.date.schedule != undefined && d.date.schedule!= "") {
                d.date.schedule = new Date(d.date.schedule);
            } else {
                d.date.schedule = d.date.start;
            }*/

            if (!(d.date.start instanceof Date) || !(d.date.end instanceof Date) || d.date.start.getTime() > d.date.end.getTime()) {

                console.error("invalid dates in row of dataSet \"" + i + "\" ");
                throw new Exception();
            }
            return d;
        }

        function type2(d, i) {
            //Settando status
            var start = d.date.start.getTime(),
                end = d.date.end.getTime(),
                delay = d.date.delay.getTime();

            if (d.done == true)
                d.status = 4, chartConfig.data_legend[4].label++
            else if (now < start)
                d.status = 2, chartConfig.data_legend[2].label++
            else if (now <= end && now >= start)
                d.status = 1, chartConfig.data_legend[1].label++
            else if (now >= delay)
                d.status = 3, chartConfig.data_legend[3].label++
            else
                d.status = 0, chartConfig.data_legend[0].label++;
            //Settando Posição - Evitando sobreposição
            var pos = positions.indexOf(null);
            if (pos == -1) {
                positions = positions.map(function (d) {
                    if (d != null && start > d.date.end.getTime())
                        return null;
                    return d;
                });
                var pos = positions.indexOf(null);
                if (pos == -1) {
                    chartConfig.layout.maxrow++;
                    pos = positions.push(null) - 1;//Captura ultimo indice do vetor após a inserção.
                }
            }

            d.position = pos;
            positions[pos] = d;
            return d;

        }

        chartConfig.data = chartConfig.data.map(type);

        function sortByDate(d1, d2) {
            var start1 = d1.date.start.getTime(),
                start2 = d2.date.start.getTime();
            return start1 > start2 ? 1 : (start1 < start2 ? -1 : 0);
        }

        function sortbyStatus(d1, d2) {
            return d1.status > d2.status ? -1 : (d1.status < d2.status ? 1 : sortByDate(d1, d2));
        }

        chartConfig.data.sort(sortByDate);

        chartConfig.data_legend = chartConfig.layout.texts.map(function (d, i) {
            return { name: d, color: chartConfig.layout.colors[i], label: 0 }
        });

        chartConfig.data = chartConfig.data.map(type2);

        chartConfig.data_legend = chartConfig.data_legend.map(function (d) {
            d.label *= 100 / chartConfig.data.length;
            d.label = "" + Math.round(d.label) + "%"
            return d;
        })

        chartConfig.data.sort(sortbyStatus);

        chartConfig.data = chartConfig.data.map(function (d, i) { d.id = i; return d; });

        //this.chartConfig = ;


        return chartConfig;//this;
    }
    create(chartConfig) {
        var a = this;
        this.chartConfig = chartConfig;
        this.now = chartConfig.now;
        this.svg = a.chartConfig.svg ? d3.select(a.chartConfig.parents.focus) : d3.select(a.chartConfig.parents.focus).append("svg").attr("id", chartConfig.name + "-container")

        this.svg2 = d3.select(a.chartConfig.parents.context).append("svg").attr("id", chartConfig.name + "-context");
        if (a.chartConfig.svg)
            this.chartConfig.dimensions.width = +svg.attr("width"),
                this.chartConfig.dimensions.height = +svg.attr("height");
        this.backcolor = "#F5F5F5";
        this.svg.style("background-color", this.backcolor);
        //this.svg2.style("background-color", this.backcolor);

        this.pattern = this.svg.append("defs").selectAll("pattern").data(a.chartConfig.layout.colors).enter().append("pattern").attr("id", function (d, i) { return "hachura-status-" + i }).attr("class", "diagonal-stripe-1")
            .attr("patternUnits", "userSpaceOnUse")
            .attr("width", 10).attr("height", 10)
            .attr("background-color", this.backcolor);
        this.pattern.append("path")
            .attr("d", "M 0 10 L 12 -2")
            .attr("stroke", function (d) { return d })
            .attr("stroke-width", 2);

        /*        this.pattern = this.svg.append("defs").append("pattern").attr("id", "diagonal-stripe-1")
                    .attr("patternUnits", "userSpaceOnUse")
                    .attr("width", 10).attr("height", 10)
                    .attr("background-color", this.backcolor);
        
                this.pattern.append("path")
                    .attr("d", "M 0 10 L 12 -2")
                    .attr("stroke", a.chartConfig.layout.colors[4])
                    .attr("stroke-width", 2);
        */

        this.x = d3.scaleTime();
        this.x2 = d3.scaleTime();
        this.y = d3.scaleBand().domain(range(a.chartConfig.layout.maxrow));
        var temp = d3.extent(a.chartConfig.data, function (d) { return d.date.start; });
        var temp2 = d3.extent(a.chartConfig.data, function (d) { return d.date.end });
        if (a.now.getTime() - temp[0].getTime() < 0) temp[0] = a.now;
        if (a.now.getTime() - temp2[1].getTime() > 0) temp2[1] = a.now;
        this.x.domain([temp[0], temp2[1]]);
        this.x2.domain(this.x.domain());
        this.brush = d3.brushX().on("brush end", function () { a.brushed(a) });
        this.zoom = d3.zoom().scaleExtent([1, Infinity]).on("zoom", function () { a.zoomed(a) });

        this.zoomRect = a.svg.append("rect")
            .attr("class", "zoom").attr("fill", "#FFF").style("cursor", "move").style("fill", "none").style("pointer-events", "all");

        this.focus = a.svg.append("g")
            .attr("class", "focus");
        this.context = a.svg2.append("g")
            .attr("class", "context");
        this.focusContent = a.focus.append("g").attr("class", "focuscontextContent");

        this.notifications = a.focusContent.selectAll(".notifications").data(a.chartConfig.data).enter().append("g")
            .style("cursor", "pointer")
            .attr("class", function (d) { return "notifications status-" + d.status });
        this.notifications.append("rect").attr("class", "backBar")
            .style("fill", function (d) { return "url(#hachura-status-" + d.status + ") none" })

        this.notifications.append("rect").attr("class", "progressBar")
            .attr("fill", function (d) { return a.chartConfig.layout.colors[d.status] });

        this.nowLine = a.focus.append("g");
        this.nowLine.append("line")
            .attr("fill", "none")
            .attr("stroke", "#222")
            .attr("stroke-width", "2")
            .attr("stroke-dasharray", "5 10");

        this.backgroundContext = a.context.append("rect").attr("class", "backgroundContext");

        this.contextContent = a.context.append("g").attr("class", "contextContent");

            this.nowLine2 = a.context.append("g");
            this.nowLine2.append("line")
                .attr("fill", "none")
                .attr("stroke", "#222")
                .attr("stroke-width", "2")
                .attr("stroke-dasharray", "2 5");

        

        

        this.card = {}

        this.card.create = function () {
            var b = this;
            this.out_dark = a.svg.append("rect")
                .attr("fill", "#000")
                .attr("opacity", 0)
                //.attr("opacity",0.4)
                //.attr("width",a.chartConfig.dimensions.width)
                //.attr("height",a.chartConfig.dimensions.height);
                .attr("width", 0)
                .attr("height", 0)
                .on("click", function () {
                    a.card.disable(0, 500);
                });
            this.all = a.svg.append("g").attr("class", "card");
            //Rects of card
            this.rects = this.all.append("g").attr("class", "cardrects");
            this.rects.append("rect").attr("class", "background")
                .attr("fill", "#fff")
                .attr("stroke-width", "2");
            this.rects.append("rect").attr("class", "backBar")
                .attr("stroke-width", 0);
            this.rects.append("rect").attr("class", "progressBar");

            //Content of Card
            this.content = this.all.append("g").attr("class", "cardContent").attr("opacity", 0);
            this.content.append("text").attr("class", "id").attr("opacity", 0);

            //Status Info(Exclamation)
            this.content.append("g").attr("class", "statusInfo");
            this.content.select(".statusInfo").append("rect");
            this.content.select(".statusInfo").append("text").attr("class", "lblstatus")
                .attr("fill", "#FFF")
            this.content.select(".statusInfo").append("g").attr("class", "exclamationContainer");
            //exclamation(this.content.select(".statusInfo").select(.exclamationContainer),100,100,"#FFF");

            // Tittle of Card
            this.content.append("text").attr("class", "tittle")
                .style("font-weight", "bold");
            //.attr("text-anchor", "start");

            // Dates of task (start, end, delay, schedule)
            this.content.append("g").attr("class", "datesInfo");
            //Start
            //End or delay
            //Schedule
            this.content.select(".datesInfo").selectAll("text").data([
                "start", "endOrDelay"//,"schedule"
            ]).enter().append("text").attr("class", function (d) { return d })
                .attr("y", function (d, i) { return "" + i + "em" }).text(function (d) { return d })



            // Percent of done
            this.content.append("g").attr("class", "percentInfo");
            this.content.select(".percentInfo").append("text").attr("class", "info info1")
                .attr("text-anchor", "start").text(a.chartConfig.layout.percent_text.match(/^[^%]{1,}(?=%)/)[0]);
            this.content.select(".percentInfo").append("text").attr("class", "percent")
                .style("font-weight", "bold")
            //.attr("text-anchor", "middle");
            this.content.select(".percentInfo").append("text").attr("class", "info info2")
                .attr("text-anchor", "start").text(a.chartConfig.layout.percent_text.match(/(?<=%)[^%]{1,}$/)[0]);

            // Description (Optional)
            this.content.append("g").attr("class", "desc")
                .attr("text-anchor", "start");

            // Buttons in Botton
            this.content.append("g").attr("class", "buttons");
            this.content.select(".buttons").append("text").attr("class", "or")
                .attr("text-anchor", "middle")
                .style("cursor", "pointer")
                .text("ou")

            // Button schedule
            /*this.content.select(".buttons").append("g").attr("class", "schedule")
                .style("cursor","pointer")
                .append("rect")
                .attr("fill", "#ccc");
            this.content.select(".buttons").select(".schedule").append("text")
                .attr("text-anchor", "middle")
                .attr("dy", "1.25em")
                .attr("fill", "#000")
                .text("Agendar tarefa");*/

            // Button Do task
            this.content.select(".buttons").append("g").attr("class", "goto")
                .style("cursor", "pointer")
                .append("rect")
                .attr("fill", "#ccc");
            this.content.select(".buttons").select(".goto").append("text")
                .attr("text-anchor", "middle")
                .attr("fill", "#000")
                .text(a.chartConfig.layout.buttonDoTask_text);//Acessar Tarefa

            this.closer = this.all.append("g").attr("class", "closer").style("cursor", "pointer").on("click", function () { b.disable(0, 400) }).attr("opacity", 0);

            this.closer.append("path").attr("fill", "#FFF").attr("d", closerBack());
            this.closer.append("path").attr("fill", "#777").attr("d", closer());


            this.content.select(".goto").on("click", function () { var data = a.chartConfig.data[a.card.content.select(".id").text()]; chartConfig.interactions.button(this, data) });



            //this.content.select(".schedule").on("click", function () { var data = a.chartConfig.data[a.card.content.select(".id").text()]; chartConfig.interactions.button(this, data) });

            this.active = false;
        }

        this.card.draw = function () {
            var b = this;

            if (a.chartConfig.dimensions.vertical) {
                if (a.width / 2 > 300)
                    this.width = 600
                else
                    this.width = a.width;
                this.size = this.width / 2;
                this.center = true;
            } else {
                if ((a.height * .7) > 300) {
                    this.size = 300
                } else if ((a.height * .7) < 197) {
                    if (197 > a.chartConfig.dimensions.height)
                        this.size = a.chartConfig.dimensions.height
                    else
                        this.size = 197;
                    this.center = true;
                } else {
                    this.size = a.height * .7;
                }
                this.width = this.size * 6 / 3;
            }
            var y = 0;

            this.all.attr("transform", "translate(" + (-this.width - a.margin.left) + ",0)");



            //Rects of Card
            this.rects.select(".background")
                //.attr("width", this.width)
                //.attr("height", this.size)
                .attr("stroke", "#000")
                .attr("rx", a.y.bandwidth() / 4)
                .attr("ry", a.y.bandwidth() / 4);
            this.rects.select(".backBar")
                //.attr("width", this.width)
                //.attr("height", this.size*.15)
                .attr("stroke", "#000")
                .attr("rx", a.y.bandwidth() / 4)
                .attr("ry", a.y.bandwidth() / 4);
            this.rects.select(".progressBar")
                //.attr("width", this.width*.75)
                //.attr("height", this.size*.15)
                .attr("rx", a.y.bandwidth() / 4)
                .attr("ry", a.y.bandwidth() / 4);

            this.closer.attr("transform", "translate(" + (this.width - this.size * .11) + "," + this.size * .04 + ") scale(" + this.size * .0007 + "," + this.size * .0007 + ")");

            y += this.size * .15;

            //Status Info(Exclamation)
            if (a.chartConfig.dimensions.mini) {
                this.content.select(".statusInfo")
                    .attr("transform", "translate(" + this.width + "," + this.size * .5 + ")");
                this.content.select(".statusInfo").select("rect")
                    //.attr("width", this.width)
                    .attr("height", this.size * 0.13)
                this.content.select(".statusInfo").select("text")
                    .attr("transform", "translate(" + this.width * .06 + "," + this.size * .0975 + ")")
                    .attr("font-size", this.size * .07)
                this.content.select(".statusInfo").select(".exclamationContainer")
                    .attr("transform", "translate(" + this.width * .01 + "," + this.size * .028 + ")");
            } else {
                this.content.select(".statusInfo")
                    .attr("transform", "translate(" + this.width * .5 + "," + this.size * .22 + ")");
                this.content.select(".statusInfo").select("rect")
                    //.attr("width", this.width * .5)
                    .attr("height", this.size * .1);
                this.content.select(".statusInfo").select("text")
                    .attr("transform", "translate(" + this.width * .06 + "," + this.size * .075 + ")")
                    .attr("font-size", this.size * .05)
                this.content.select(".statusInfo").select(".exclamationContainer")
                    .attr("transform", "translate(" + this.width * .01 + "," + this.size * .015 + ")");
            }
            if (!this.exclamationCreated)
                exclamation(this.content.select(".statusInfo").select(".exclamationContainer"), this.size * .08, this.size * .08, "#FFF"), this.exclamationCreated = true;
            else
                exclamationRefatoring(this.content.select(".statusInfo").select(".exclamationContainer"), this.size * .08, this.size * .08, "#FFF");

            // Tittle of Card
            this.content.select(".tittle")
                .attr("font-size", this.size * .08)
                .attr("transform", "translate(" + this.width * .02 + "," + (y + this.size * .15) + ")");

            y += this.size * .15;

            //Dates  of Card
            this.content.select(".datesInfo")
                .attr("transform", "translate(" + this.width * .04 + "," + (y + this.size * .06) + ")")
                .attr("font-size", this.size * .04)
            y += this.size * .06;
            // Percent of done
            this.content.select(".percentInfo")
                .attr("font-size", this.size * .05)
                .attr("transform", "translate(" + this.width * .02 + "," + (y + this.size * .14) + ")");

            b.percentSpace = {
                info1: document.querySelector("#" + chartConfig.name + "-container").querySelector(".info1").getBoundingClientRect().width,
            }

            this.content.select(".percentInfo").selectAll("text")
                .attr("x", function (d, i) {
                    switch (i) {
                        case 0: return 0;
                        case 1: return b.percentSpace.info1 + b.size * .005;
                        case 2: return a.card.width * .32;
                    }
                })

            y += this.size * .14;

            // Description (Optional)
            this.content.select(".desc")
                .attr("font-size", this.size * .04)
                .attr("transform", "translate(" + this.width * .02 + "," + (y + this.size * .03) + ")");
            y += this.size * .03;
            // Buttons in Botton
            this.content.select(".buttons")
                .attr("transform", "translate(0," + this.size * .85 + ")");

            this.content.select(".buttons").select(".or")
                .attr("font-size", this.size * .08)
                .attr("dy", ".9em")
                .attr("transform", "translate(" + this.width * .5 + ",0)");

            this.content.select(".buttons").select(".goto")
                .attr("transform", "translate(" + this.width * .05 + ",0)");
            this.content.select(".buttons").select(".goto").select("rect")
                .attr("width", this.width * .35)
                .attr("height", this.size * .1)
            this.content.select(".buttons").select(".goto").select("text")
                .attr("font-size", this.size * .04)
                .attr("dy", "1.5em")
                .attr("transform", "translate(" + this.width * .175 + ",0)");

            /*this.content.select(".buttons").select(".schedule")
                .attr("transform", "translate(" + this.width * .6 + ",0)");
            this.content.select(".buttons").select(".schedule").select("rect")
                .attr("width", this.width * .35)
                .attr("height", this.size * .1)
            this.content.select(".buttons").select(".schedule").select("text")
                .attr("font-size", this.size * .04)
                .attr("transform", "translate(" + this.width * .175 + ",0)");*/
        }

        this.card.activate = function (data) {
            var b = a.card;
            var before = 0;
            if (b.active != false) {
                before += b.disable(before, 200);
            }
            if (!a.bottomLegend.marked[data.status]) {
                a.bottomLegend.setoption();
            }
            before = b.rect_in_x(data, before);
            before = b.extend_card(data, before, 1000);
            b.active = data;
        }

        this.card.disable = function (before, transition) {
            var b = a.card;
            if (b.active == false)
                return
            before = b.rect_in_x(b.active, before, transition);
            b.all
                .transition().delay(before).duration(0)
                .attr("transform", function () { return "translate(" + (-document.querySelector(".card").getBoundingClientRect().width) + ",0)" });

            b.rects.select(".background")
                .transition().delay(before + 10).duration(0)
                .attr("width", 0)
                .attr("height", 0);
            b.rects.select(".progressBar")
                .transition().delay(before + 10).duration(0)
                .attr("width", 0)
                .attr("height", 0);
            b.rects.select(".backBar")
                .transition().delay(before + 10).duration(0)
                .attr("width", 0)
                .attr("height", 0);
            b.content.select(".statusInfo").select("rect")
                .transition().delay(before + 10).duration(0)
                .attr("width", 0);

            b.active = false;
            return before + 2;
        }

        this.card.rect_in_x = function (data, before, transition) {
            var b = a.card;
            if (isNaN(before)) before = 0;
            if (isNaN(transition)) transition = 0;
            b.all
                .transition().delay(before).duration(transition)
                .attr("transform", "translate(" + (a.x(data.date.start) + a.margin.left) + "," + (a.y(data.position) + a.margin.top) + ")");

            b.out_dark
                .transition().delay(before).duration(transition)
                .attr("opacity", 0);

            b.out_dark
                .transition().delay(before + transition + 10)
                .attr("width", 0)
                .attr("height", 0);

            b.closer
                .transition().delay(before).duration(transition * .2)
                .attr("opacity", 0);

            b.content
                .transition().delay(before).duration(transition * .2)
                .attr("opacity", 0);

            b.rects.select(".background")
                .transition().delay(before).duration(transition)
                .attr("stroke", a.chartConfig.layout.colors[data.status])
                .attr("width", a.x(data.date.end) - a.x(data.date.start))
                .attr("fill", a.backcolor)
                .attr("height", a.y.bandwidth());
            b.rects.select(".progressBar")
                .transition().delay(before).duration(transition)
                .attr("fill", a.chartConfig.layout.colors[data.status])
                .attr("width", (a.x(data.date.end) - a.x(data.date.start)) * data.percent)
                .attr("height", a.y.bandwidth());
            b.rects.select(".backBar")
                .transition().delay(before).duration(transition)
                .attr("fill", a.backcolor)
                .style("fill", "url(#hachura-status-" + data.status + ")" + a.backcolor)

                .attr("width", a.x(data.date.end) - a.x(data.date.start))
                .attr("height", a.y.bandwidth());
            return before + transition + 1;
        }

        this.card.reposition = function (x) {
            // Tittle of Card
            this.content.select(".tittle")
                .attr("transform", "translate(" + this.width * .02 + "," + (x + this.size * .15) + ")");

            x += this.size * .15;

            //Dates  of Card
            this.content.select(".datesInfo")
                .attr("transform", "translate(" + this.width * .04 + "," + (x + this.size * .06) + ")")
            x += this.size * .06;
            // Percent of done
            this.content.select(".percentInfo")
                .attr("transform", "translate(" + this.width * .02 + "," + (x + this.size * .14) + ")");


            x += this.size * .14;
        }

        this.card.extend_card = function (data, before, transition) {
            var b = this;

            b.out_dark
                .attr("width", a.chartConfig.dimensions.width)
                .attr("height", a.chartConfig.dimensions.height);

            b.out_dark
                .transition().delay(before).duration(transition)
                .attr("opacity", 0.4)

            if (isNaN(before)) before = 0;
            if (isNaN(transition)) transition = 0;
            var x, y;
            if (b.center) {
                x = (a.chartConfig.dimensions.width - this.width) / 2, y = (a.chartConfig.dimensions.height - this.size) / 2
            } else {
                x = a.x(data.date.start), y = a.y(data.position);
                if (x + b.width > a.width)
                    x = a.width - b.width;
                else if (x < -a.margin.left)
                    x = 0;
                if (y + b.size > a.height)
                    y = a.height - b.size;
            }
            //Rects of card
            b.all
                .transition().delay(before).duration(transition)
                .attr("transform", "translate(" + x + "," + y + ")");
            b.rects.select(".background")
                .transition().delay(before).duration(transition)
                .attr("width", b.width)
                .attr("height", b.size)
                .attr("fill", "#fff");
            b.rects.select(".progressBar")
                .transition().delay(before).duration(transition)
                .attr("width", b.width * data.percent)
                .attr("height", b.size * .15);
            b.rects.select(".backBar")
                .transition().delay(before).duration(transition)
                .attr("width", b.width)
                .style("fill", "url(#hachura-status-" + data.status + ")#fff")
                .attr("height", b.size * .15);
            //Content of Card

            // Tittle of Card
            b.content.select(".tittle")
                //.transition().delay(before).duration(transition)
                .text(data.action + " " + data.name);

            //Status info
            var temp = a.chartConfig.layout.texts2[data.status];
            if (temp != undefined && temp != "") {
                if (!a.chartConfig.dimensions.mini) {

                    if (temp != undefined && temp != "" && document.querySelector(".tittle").getBoundingClientRect().width >= this.width * .50) {
                        b.content.select(".statusInfo")
                            .attr("transform", "translate(" + b.width + "," + b.size * .34 + ")")
                            .select("rect")
                            .attr("width", 0)
                        b.content.select(".statusInfo")
                            .transition().delay(before).duration(transition)
                            .attr("transform", "translate(" + b.width * .5 + "," + b.size * .34 + ")")
                            .attr("opacity", 1);
                    } else {
                        b.content.select(".statusInfo")
                            .attr("transform", "translate(" + b.width + "," + b.size * .22 + ")")
                            .select("rect")
                            .attr("width", 0)
                        b.content.select(".statusInfo")
                            .transition().delay(before).duration(transition)
                            .attr("transform", "translate(" + b.width * .5 + "," + b.size * .22 + ")")
                            .attr("opacity", 1);
                    }

                    b.content.select(".statusInfo").select("rect")
                        .transition().delay(before).duration(transition)
                        .attr("width", b.width * .5)
                        .attr("fill", a.chartConfig.layout.colors[data.status])
                } else {
                    b.content.select(".statusInfo")
                        .attr("transform", "translate(0," + b.size * .6 + ")")
                        .select("rect")
                        .attr("width", b.width)
                        .attr("fill", a.chartConfig.layout.colors[data.status])
                    b.content.select(".statusInfo")
                        .transition().delay(before).duration(transition)
                        .attr("opacity", 1);

                }
                b.content.select(".statusInfo").select("text")
                    .transition().delay(before).duration(transition)
                    .text(temp);
            } else {
                b.content.select(".statusInfo")
                    .transition().delay(before).duration(transition)
                    .attr("opacity", 0);
            }

            //Dates  of Card
            this.content.select(".datesInfo").selectAll("text")
                .transition().delay(before).duration(transition)
                .attr("opacity", function (d, i) {
                    switch (i) {
                        case 0: case 1: return 1;
                        //   case 2:return (!data.done) && data.date.schedule.getTime()>data.date.start.getTime()&&a.chartConfig.now.getTime()<data.date.delay.getTime()?1:0;
                    }
                })
                .attr("fill", function (d, i) {
                    switch (i) {
                        case 0: return "#444";
                        case 1: return data.status == 3 ? "#F00" : "#444";
                        //    case 2:return (a.chartConfig.now.getTime()>=data.date.schedule.getTime()?"#F22":"#444");
                    }
                })
                .text(function (d, i) {
                    var start = data.date.start.toLocaleString("pt-br"),
                        end = data.date.end,
                        now = a.chartConfig.now;
                    //  schedule = data.date.schedule.toLocaleString();
                    if (end.getTime() < now.getTime()) end = data.date.delay;
                    end = end.toLocaleString("pt-br");

                    switch (i) {
                        case 0: return a.chartConfig.layout.initDate_text + start.substr(0, start.length - 3);
                        case 1: return (data.status == 3 ? a.chartConfig.layout.closedDate_text : a.chartConfig.layout.endDate_text) + end.substr(0, start.length - 3);
                        // case 2:return "Sua meta "+(now.getTime()>=data.date.schedule.getTime()?"era":"é")+" realizar em: "+schedule;
                    }
                })
            if (data.percent > a.chartConfig.layout.percent_min || data.status == 4)
                b.content.select(".percentInfo").attr("opacity", 1)
            else
                b.content.select(".percentInfo").attr("opacity", 0)
            b.content.select(".percent")
                .text(("" + (data.percent * 100)).substr(0, 4) + "%");

            this.percentSpace.percent = document.querySelector("#" + chartConfig.name + "-container").querySelector(".percent").getBoundingClientRect().width
            this.content.select(".percentInfo").select(".info2").attr("x", b.percentSpace.info1 + b.percentSpace.percent + b.size * .01)


            var font = b.size * .04;
            var nletters = b.width * 1.3 / font;
            var textvector = String.linebroke(data.desc, nletters);

            b.content.select(".desc")
                .selectAll("text").remove();

            b.content.select(".desc")
                .selectAll("text").data(textvector).enter().append("text")
                .transition().delay(before).duration(transition)
                .attr("dy", function (d, i) { return "" + (i * 1.3 + 1) + "em" })
                .text(function (d) { return d });

            b.content.select(".id")
                .transition().delay(before).duration(transition)
                .text(data.id);

            if (data.status == 3 || data.status == 4) {
                this.content.select(".buttons").select(".goto")
                    .attr("transform", "translate(" + this.width * .325 + ",0)")
                    .select("text").text(a.chartConfig.layout.buttonAccess_text);
            } else {
                this.content.select(".buttons").select(".goto")

                    .select("text").text(a.chartConfig.layout.buttonDoTask_text);
            }
            if (a.chartConfig.dimensions.mini) {
                this.content.select(".buttons").select(".goto")
                    .attr("transform", "translate(" + this.width * .1 + ",0)")
                    .select("rect")
                    .attr("width", this.width * .8)
                this.content.select(".buttons").select(".goto").select("text")
                    .attr("transform", "translate(" + this.width * .4 + ",0)")
                    .attr("font-size", this.size * .06)
                    .attr("dy", "1.2em")
            } else {
                this.content.select(".buttons").select(".goto")
                    .attr("transform", "translate(" + this.width * .325 + ",0)")
                    .select("rect")
                    .attr("width", this.width * .35)
                this.content.select(".buttons").select(".goto").select("text")
                    .attr("transform", "translate(" + this.width * .175 + ",0)")
                    .attr("font-size", this.size * .04)
                    .attr("dy", "1.6em")
            }

            b.content.transition().delay(before + transition * .7).duration(transition * .3).attr("opacity", 1);
            b.closer
                .transition().delay(before + transition * .7).duration(transition * .3)
                .attr("opacity", 1);




            return before + transition + 1;
        }

        var last = 0, laststatus = 0;
        function searchStatus(status) {
            var data = a.chartConfig.data;
            if (status != laststatus) {
                laststatus = status;
                last = 0;
            }
            var back = false;
            for (var i = last % data.length; true; i = (i + 1) % data.length) {
                if (data[i].status == status) {
                    last = i + 1;
                    return data[i];
                }
                if (back && last == i)
                    return;
                if (last == i)
                    back = true;
            }
            return null;
        }
        this.legendConfig = {
            data: chartConfig.data_legend,
            target: a.chartConfig.parents.legend,
            svg: a.chartConfig.svg,
            dimensions: {
                width: a.chartConfig.dimensions.width
            },
            layout: {
                corner: 4,
                font_size: 16,
                font: "Roboto",
                //stroke: "#000",
                stroke_width: 2,
                stroke_over: "#444",
                anchor: "middle", // start middle end
                enable_mark: true,
                label: true,
                labelcolor: "#fff"
            },
            interactions: {
                //mouseover: function (element, data) { },
                //mousemove: function (element, data) { },
                //mouseout: function (element, data) { },
                click: function (element, data) {
                    a.card.disable(0, 500);
                    //a.goto(searchStatus(status));
                },
                filter: function (element, data) {
                    a.filter(data.id, element);
                },
                unfilter: function (element, data) {
                    a.filterout(data.id, element);
                },
                unfilterAll: function () {
                    a.filterout();
                }
            },
        }


        this.bottomLegend = new BottomLegend(this.legendConfig);

        this.card.create();

        this.notifications.on("click", a.card.activate);

        this.zoomRect
            .on("click", function () {
                a.bottomLegend.setoption();
                a.card.disable(0, 500);
            });

        this.context.append("g")
            .attr("class", "axis axis--x context-axis");
        this.focus.append("g")
            .attr("class", "axis axis--x focus-axis")
        this.context.append("g")
            .attr("class", "brush")

        this.contextRects = this.contextContent.selectAll(".testRects").data(a.chartConfig.data).enter().append("rect")
            .attr("class", function (d) { return "testRects status-" + d.status; });

        return this;
    }
    draw2() {
        var a = this;

        var temp = document.querySelector(a.chartConfig.parents.context).getBoundingClientRect();
        a.chartConfig.dimensions.width2 = temp.width - $(a.chartConfig.parents.context).css("padding-left").match(/[0-9]+/)[0] - $(a.chartConfig.parents.context).css("padding-right").match(/[0-9]+/)[0];

        this.margin2 = {
            top: 5,
            right: a.chartConfig.margin.right,
            bottom: a.chartConfig.margin.bottom,
            left: a.chartConfig.margin.left
        };
        var temp = a.chartConfig.dimensions.height * a.chartConfig.layout.contextHeight
        this.chartConfig.dimensions.height2 = temp < 15 ? 15 : (temp > 30 ? 30 : temp) + a.margin2.top + a.margin2.bottom;

        this.height2 = a.chartConfig.dimensions.height2 - a.margin2.top - a.margin2.bottom;
        this.width2 = a.chartConfig.dimensions.width2 - a.margin2.left - a.margin2.right;

        this.svg2
            .attr("width", a.chartConfig.dimensions.width2)
            .attr("height", a.chartConfig.dimensions.height2)
        this.x2.range([0, a.width2])

        this.nowLine2.select("line")
            .attr("x1", 0)
            .attr("y1", 0)
            .attr("x2", 0)
            .attr("y2", a.height2);

        this.xAxis2 = d3.axisBottom(this.x2).ticks(Math.floor(a.chartConfig.dimensions.width2 / 220));

        a.nowLine2
        //    .transition().duration(transition)
            .attr("transform", "translate(" + a.x2(a.now) + ",0)");

        this.brush.extent([[0, 0], [a.width2, a.height2]]);

        this.context.attr("transform", "translate(" + a.margin2.left + "," + a.margin2.top + ")");

        function widthRect(data) {
            return a.x2(data.date.end) - a.x2(data.date.start);
        }

        this.backgroundContext
            .attr("width", a.width2)
            .attr("height", a.height2 * .5)
            .attr("transform", "translate(0," + a.height2 * .25 + ")")
            .attr("fill", a.backcolor);

        this.contextRects
            .attr("transform", function (d) { return "translate(" + a.x2(d.date.start) + "," + a.height2 * .15 + ")" })
            .attr("width", widthRect)
            .attr("height", a.height2 * .7)
            .attr("rx", a.height2 / 3 > 10 ? 10 : a.height2 / 3)
            .attr("ry", a.height2 / 3 > 10 ? 10 : a.height2 / 3)
            .attr("stroke", "#ddd")
            .attr("stroke-width", ".5")
            .attr("fill", function (d) { return a.chartConfig.layout.colors[d.status] });;

        this.context.select(".context-axis")
            .attr("transform", "translate(0," + a.height2 + ")")
            .call(a.xAxis2);

        this.context.select(".brush")
            .call(a.brush)
            .call(a.brush.move, a.x.range());
        
        this.legendConfig.dimensions.width = this.width2

        this.bottomLegend.draw();
        
        a.draw2_flag = true;

        return this;

    }
    draw() {
        var a = this;

        document.definewidth(chartConfig, chartConfig.sugest.width, chartConfig.sugest.height, chartConfig.sugest.windowProp, chartConfig.sugest.chartProp, chartConfig.parents.focus);

        this.margin = {
            top: a.chartConfig.margin.top,
            right: a.chartConfig.margin.right,
            bottom: a.chartConfig.margin.bottom,
            left: a.chartConfig.margin.left
        };




        //this.chartConfig.dimensions.height = a.chartConfig.dimensions.height*(1-a.chartConfig.layout.contextHeight);


        this.width = a.chartConfig.dimensions.width - a.margin.left - a.margin.right;
        this.height = a.chartConfig.dimensions.height - a.margin.top - a.margin.bottom;

        if (!a.draw2_flag) {
            var temp = document.querySelector("#accordion_bar").getBoundingClientRect();
            a.chartConfig.dimensions.width2 = temp.width - 2*$("#accordion_bar").css("padding-left").match(/[0-9]+/)[0] - 2*$("#accordion_bar").css("padding-right").match(/[0-9]+/)[0];

            this.margin2 = {
                top: 5,
                right: a.chartConfig.margin.right,
                bottom: a.chartConfig.margin.bottom,
                left: a.chartConfig.margin.left
            };
            var temp = a.chartConfig.dimensions.height * a.chartConfig.layout.contextHeight
            this.chartConfig.dimensions.height2 = temp < 15 ? 15 : (temp > 30 ? 30 : temp) + a.margin2.top + a.margin2.bottom;

            this.height2 = a.chartConfig.dimensions.height2 - a.margin2.top - a.margin2.bottom;
            this.width2 = a.chartConfig.dimensions.width2 - a.margin2.left - a.margin2.right;

            this.brush.extent([[0, 0], [this.width2, this.height2]]);
        }
        

        this.svg
            .attr("width", a.chartConfig.dimensions.width)
            .attr("height", a.chartConfig.dimensions.height)



        this.x.range([0, a.width]),
            this.y.rangeRound([0, a.height]).padding(a.height > 200 ? 0.4 : 0.1);

        this.nowLine.select("line")
            .attr("x1", 0)
            .attr("y1", 0)
            .attr("x2", 0)
            .attr("y2", a.height);

        this.xAxis = d3.axisBottom(this.x).ticks(Math.floor(a.chartConfig.dimensions.width / 110));

        this.zoom.translateExtent([[0, 0], [a.width, a.height]])
            .extent([[0, 0], [a.width, a.height]]);

        this.focus.attr("transform", "translate(" + a.margin.left + "," + a.margin.top + ")");

        this.notifications.select(".backBar")
            .attr("rx", a.y.bandwidth() / 4)
            .attr("ry", a.y.bandwidth() / 4);

        this.notifications.select(".progressBar")
            .attr("rx", a.y.bandwidth() / 4)
            .attr("ry", a.y.bandwidth() / 4);

        this.transformElements();



        this.focus.select(".focus-axis")
            .attr("transform", "translate(0," + a.height + ")")
            .call(a.xAxis);

        this.zoomRect
            .attr("width", a.width)
            .attr("height", a.height)
            .attr("transform", "translate(" + a.margin.left + "," + a.margin.top + ")")
            .call(a.zoom);
        this.card.draw();

        this.bottomLegend.setoption();
        this.card.disable();
        //this.reset();

        return this;
    }
    resize(width, height) {
        var a = this;
        a.chartConfig.dimensions.width = width,
            a.chartConfig.dimensions.height = height;
        document.definewidth(a.chartConfig, a.chartConfig.sugest.width, a.chartConfig.sugest.height, a.chartConfig.sugest.windowProp, a.chartConfig.sugest.chartProp, a.chartConfig.parents.context);
        a.chartConfig.dimensions.width2 = a.chartConfig.dimensions.width;
        a.chartConfig.dimensions.width = undefined;
        a.chartConfig.dimensions.height = undefined;
        document.definewidth(a.chartConfig, a.chartConfig.sugest.width, a.chartConfig.sugest.height, a.chartConfig.sugest.windowProp, a.chartConfig.sugest.chartProp, a.chartConfig.parents.focus);
        this.draw();
        return this;
    }
    filter(status, element) {
        var a = this;
        a.svg.selectAll(".notifications").transition().duration(500).attr("opacity", 0.2)
        a.svg2.selectAll(".testRects").transition().duration(500).attr("opacity", 0.05)

        a.bottomLegend.marked.map(function (d, i) {
            if (d) {
                a.svg.selectAll(".status-" + i).transition().duration(500).attr("opacity", 1)
                a.svg2.selectAll(".status-" + i).transition().duration(500).attr("opacity", 1)
            }
        });
        a.bottomLegend.legend/*.attr("opacity", function(d,i){
                if(a.bottomLegend.marked[i]==true)
                    return 0.5;
                else   
                    return 1;
            })*/.attr("style", function (d, i) {
            if (a.bottomLegend.marked[i] == true)
                return "cursor:url('" + a.chartConfig.cursors.subber + "'),auto";
            else
                return "cursor:url('" + a.chartConfig.cursors.adder + "'),auto";
        });

    }
    filterout(status, element) {
        var a = this;
        if (status != undefined) {
            a.bottomLegend.marked.map(function (d, i) {
                if (d == false) {
                    a.svg.selectAll(".notifications.status-" + i).transition().duration(500).attr("opacity", 0.2)
                    a.svg2.selectAll(".testRects.status-" + i).transition().duration(500).attr("opacity", 0.05)
                }
            });
            a.bottomLegend.legend
                .attr("style", function (d, i) {
                    if (a.bottomLegend.marked[i] == true)
                        return "cursor:url('" + a.chartConfig.cursors.subber + "'),auto";
                    else
                        return "cursor:url('" + a.chartConfig.cursors.adder + "'),auto";
                });
        } else {
            if (a.bottomLegend.legend)
                a.bottomLegend.legend.attr("style", "cursor:url('" + a.chartConfig.cursors.filter + "'),auto");
            a.svg.selectAll(".notifications").transition().duration(500).attr("opacity", 1);
            a.svg2.selectAll(".testRects").transition().duration(500).attr("opacity", 1);
        }
    }
    goto(data, period) {
        if (!data)
            return;
        var a = this;
        this.gotoperiod(data.date.start, data.date.end, period);
        a.card.activate(data);
    }
    gotoperiod(init, end, period) {
        var a = this;
        if (period == undefined)
            period = 10;
        var s = [
            new Date(init.getFullYear(), init.getMonth(), init.getDate() - period),
            new Date(end.getFullYear(), end.getMonth(), end.getDate() + period)
        ];
        s = s.map(function (d) {
            var temp = a.x2(d);
            return temp < 0 ? 0 : (temp > a.x2.range()[1] ? a.x2.range()[1] : temp);
        });
        a.x.domain(s.map(a.x2.invert, a.x2));

        a.focus.select(".axis--x").call(a.xAxis);

        a.svg.select(".zoom").call(a.zoom.transform, d3.zoomIdentity
            .scale(a.width / (s[1] - s[0]))
            .translate(-s[0], 0));

    }
    reset(period) {
        var a = this;
        if (period == undefined)
            period = 10;
        var s = [new Date(a.now.getFullYear(), a.now.getMonth(), a.now.getDate() - period),
        new Date(a.now.getFullYear(), a.now.getMonth(), a.now.getDate() + period)];
        s = s.map(function (d) {
            var temp = a.x2(d);
            return temp < 0 ? 0 : (temp > a.x2.range()[1] ? a.x2.range()[1] : temp);
        });

        a.x.domain(s.map(a.x2.invert, a.x2));

        a.focus.select(".axis--x").call(a.xAxis);

        a.transformElements(500);

        a.svg.select(".zoom").call(a.zoom.transform, d3.zoomIdentity
            .scale(a.width / (s[1] - s[0]))
            .translate(-s[0], 0));
    }
    zoomed(a, transition) {
        if (a.card.active) {
            a.card.disable(0, 500);
        }
        if (d3.event.sourceEvent && d3.event.sourceEvent.type === "brush") return; // ignore zoom-by-brush
        var t = d3.event.transform;
        temp = t;
        a.x.domain(t.rescaleX(a.x2).domain());

        a.focus.select(".axis--x").call(a.xAxis);
        //if(isNaN(a.temptransition))
        //a.temptransition = 200;
        this.transformElements();
        //if(a.draw2_flag)
        a.context.select(".brush").call(a.brush.move, a.x.range().map(t.invertX, t));
    }
    brushed(a) {
        if (a.card.active) {
            a.card.disable(0, 500);
        }
        if (d3.event.sourceEvent && d3.event.sourceEvent.type === "zoom") return; // ignore brush-by-zoom
        var s = d3.event.selection || a.x2.range();
        temp2 = s;
        a.x.domain(s.map(a.x2.invert, a.x2));

        a.focus.select(".axis--x").call(a.xAxis);
        //var transition = a.temptransition;
        //a.temptransition = 0;
        a.transformElements();

        a.svg.select(".zoom").call(a.zoom.transform, d3.zoomIdentity
            .scale(a.width / (s[1] - s[0]))
            .translate(-s[0], 0));
        //a.temptransition = transition;
    }
    transformElements(transition) {
        if (isNaN(transition))
            transition = 0;
        var a = this;
        function widthRect(data) {
            return a.x(data.date.end) - a.x(data.date.start);
        }
        function transformRect(data, i) {
            return "translate(" + (a.x(data.date.start)) + "," + a.y(data.position) + ")";
        }

        a.notifications
            //.transition().duration(transition)
            .attr("transform", transformRect)
        a.notifications.select(".backBar")
            //.transition().duration(transition)
            .attr("width", widthRect)
            .attr("height", a.y.bandwidth());
        a.notifications.select(".progressBar")
            //.transition().duration(transition)
            .attr("width", function (d) { return widthRect(d) * d.percent })
            .attr("height", a.y.bandwidth());

        a.nowLine
        //    .transition().duration(transition)
            .attr("transform", "translate(" + a.x(a.now) + ",0)");

    }

}
/*
var chartConfig = {
    name: "multiGanttSubjects",
    target: "body",
    data: [
        { subject: "subject1", link: "" /Link to Subject's Analytics/, data: []/ Data of GanttChart w / },
    ],
    dimensions: {
        width: 1200,
        height: 600,
    },
    margin: {
        top: 20, bottom: 20, left: 20, right: 20,
    },
    layout: {
        colors: ["#FF9001", "#dfbd31", "#D6D6D6", "#f44336", "#3BA51A"],
        texts: ["Atrasada", "No prazo", "Planejada", "Perdida", "Concluída"],
        size: 50,
        font_size: 16,
        font_weight: "bold",
        font: "roboto",
        background_color: "#F5F5F5",
        font_color: "#000000",
        name_percent:0.2
    },
    interactions: {
        mouseover: function (element, data) { },
        mousemove: function (element, data) { },
        mouseout: function (element, data) { },
        click: function (element, data) { },
    },
    tooltip: {
        text: ""
    },
}
*/
var multiGanttCont = 0;
class MultiGanttChart {
    constructor(chartConfig) {
        this.create(MultiGanttChart.validData(chartConfig)).draw();
    }
    static validData(chartConfig) {
        if (chartConfig == undefined || chartConfig.data == undefined) {
            console.error("DataSet Invalid");
            throw new Exception();
        }
        if (chartConfig.name == undefined) chartConfig.name = "GanttChart" + (ganttCont++);
        if (chartConfig.target == undefined) chartConfig.target = "body";

        if (chartConfig.margin == undefined) chartConfig.margin = {};

        if (chartConfig.layout == undefined) chartConfig.layout = {};
        if (chartConfig.layout.colors == undefined)
            chartConfig.layout.colors = ["#AD1111", "#FAA916", "#0B4F6C", "#343434", "#00993F"]
        if (chartConfig.layout.texts == undefined || chartConfig.layout.texts.length != chartConfig.layout.colors.length)
            chartConfig.layout.texts = ["Atrasada", "Dentro do Prazo", "Pendência Futura", "Perdida", "Concluída"];
        if (chartConfig.layout.size == undefined) chartConfig.layout.size = 50;
        if (chartConfig.layout.font_size == undefined) chartConfig.layout.font_size = 16;
        if (chartConfig.layout.font == undefined) chartConfig.layout.font = "Roboto";
        if (chartConfig.layout.background_color == undefined) chartConfig.layout.background_color = "none";

        document.definewidth(chartConfig, 1200, chartConfig.layout.size * 1.1 * chartConfig.data.length);

        chartConfig.data = chartConfig.data.map(function (d, i) {
            if (d.data == undefined) {
                console.error("DataSet Invalid row:'" + i + "'");
                throw new Exception();
            }

            chartConfig.now = new Date();
            var now = chartConfig.now.getTime();

            function type(d, i) {
                //Validação linha a linha
                if (d == undefined)
                    return
                if (d.date == undefined ||
                    d.date.start == undefined ||
                    d.date.end == undefined) {
                    console.error("invalid row of dataSet \"" + i + "\" ");
                    throw new Exception();
                }
                //Configurando datas
                if (typeof d.date.start == "string") {
                    d.date.start = new Date(d.date.start);
                }

                if (typeof d.date.end == "string") {
                    d.date.end = new Date(d.date.end);
                }

                if (d.date.delay != undefined) {
                    if (typeof d.date.delay == "string")
                        d.date.delay = new Date(d.date.delay);
                } else {
                    d.date.delay = d.date.end;
                }

                if (!(d.date.start instanceof Date) || !(d.date.end instanceof Date) || d.date.start.getTime() > d.date.end.getTime()) {
                    console.error("invalid dates in row of dataSet \"" + i + "\" ");
                    throw new Exception();
                }
                return d;
            }
            function type2(d, i) {
                //Settando status
                var start = d.date.start.getTime(),
                    end = d.date.end.getTime(),
                    delay = d.date.delay.getTime();

                if (d.done == true)
                    d.status = 4
                else if (now < start)
                    d.status = 2
                else if (now <= end && now >= start)
                    d.status = 1
                else if (now >= delay)
                    d.status = 3
                else
                    d.status = 0;
                return d;

            }

            d.data = d.data.map(type);

            function sortByDate(d1, d2) {
                var start1 = d1.date.start.getTime(),
                    start2 = d2.date.start.getTime();
                return start1 > start2 ? 1 : (start1 < start2 ? -1 : 0);
            }

            d.data.sort(sortByDate);

            var temp = d3.extent(d.data, function (d) { return d.date.start; });
            var temp2 = d3.extent(d.data, function (d) { return d.date.end });
            if (chartConfig.now.getTime() - temp[0].getTime() < 0) temp[0] = a.now;
            if (chartConfig.now.getTime() - temp2[1].getTime() > 0) temp2[1] = a.now;
            d.domain = [temp[0], temp2[1]];

            d.data = d.data.map(type2);
            function sortbyStatus(d1, d2) {
                return d1.status > d2.status ? -1 : (d1.status < d2.status ? 1 : sortByDate(d1, d2));
            }
            d.data.sort(sortbyStatus);

            d.data = d.data.map(function (d, i) { d.id = i; return d; });

            if (d.name == undefined) d.name = "auto-subject" + i;
            return d;
        });

        chartConfig.data.sort(function (d1, d2) {
            return d1.domain[1] > d2.domain[1] ? 1 : (d1.domain[1] < d2.domain[0] ? -1 : 0);
        });

        chartConfig.domain = [0, chartConfig.data[chartConfig.data.length - 1].domain[1]];

        chartConfig.data.sort(function (d1, d2) {
            return d1.domain[0] > d2.domain[0] ? 1 : (d1.domain[0] < d2.domain[0] ? -1 : 0);
        });

        chartConfig.domain[0] = chartConfig.data[0].domain[0];

        chartConfig.interactions = d3.validEvents(chartConfig.interactions);
        return chartConfig;
    }
    create(chartConfig) {
        var a = this;
        this.chartConfig = chartConfig;
        var a = this;
        this.svg = data.svg ? d3.select(chartConfig.target) : d3.select(chartConfig.target).append("svg").attr("id", a.chartConfig.name);
        this.now = new Date();

        this.g = this.svg.append("g").attr("class", "multigantt-g");
        this.x = d3.scaleTime().domain(chartConfig.domain);
        this.y = d3.scaleBand().domain(range(a.chartConfig.data.length));
        this.svg.style("background-color", this.chartConfig.layout.background_color);

        this.context = this.g.append("g").attr("class", "context");
        this.subjects = this.context.selectAll(".subject").data(a.chartConfig.data).enter().append("g").attr("class", function (d, i) { "subject subject-" + i })

        this.subjects.append("rect").attr("class", "backGround").attr("fill", this.chartConfig.layout.background_color);

        this.tasks = this.subjects.append("g").attr("class", "subject-tasks-g")
            .selectAll(".task").data(function (d) { return d.data }).enter().append("rect").attr("class", "task")
            .attr("fill", function (d) { return chartConfig.layout.colors[d.status] });

        this.subjects.append("text").attr("class", "subject-name")
            .style("font-family", a.chartConfig.layout.font)
            .style("font-size", "" + a.chartConfig.layout.font_size + "px")
            .style("font-style", "normal")
            .style("font-weight", "300")
            .style("line-height", "normal")
            .text(function (d) { return d.name; });


        this.nowLine = this.subjects.select(".subject-tasks-g").append("g");
        this.nowLine.append("line");


        return this;
    }
    draw() {
        var a = this;
        this.sobreposition = false;
        this.width = this.chartConfig.dimensions.width * 0.98 - this.getNameWidth();
        if (this.width < this.chartConfig.dimensions.width * .5)
            this.width = this.chartConfig.dimensions.width * 0.98, this.sobreposition = true;
        this.height = this.chartConfig.dimensions.height;

        this.chartConfig.margin.left = this.chartConfig.dimensions.width * 0.01;
        this.chartConfig.margin.right = this.chartConfig.dimensions.width * 0.01;
        this.chartConfig.margin.top = 0;
        this.chartConfig.margin.bottom = 0;

        this.x.range([0, this.width]);
        this.y.range([0, this.height]).padding(0.1);

        //if(a.chartConfig.layout.size>a.y.bandwidth())a.chartConfig.layout.size = a.y.bandwidth();

        this.svg
            .attr("width", a.chartConfig.dimensions.width)
            .attr("height", a.chartConfig.dimensions.height);

        this.g.attr("transform", "translate(" + a.chartConfig.margin.left + "," + a.chartConfig.margin.top + ")")

        this.nowLine
            .attr("transform", "translate(" + this.x(this.chartConfig.now) + ",0)")
            .select("line")
            .attr("fill", "none")
            .attr("stroke", "#222")
            .attr("stroke-width", "2")
            .attr("stroke-dasharray", "5 10")
            .attr("x1", 0)
            .attr("y1", 0)
            .attr("x2", 0)
            .attr("y2", a.y.bandwidth);
        this.subjects.attr("transform", function (d, i) { return "translate(0," + (a.y(i) + (a.y.bandwidth() - a.chartConfig.layout.size) / 2) + ")" })

        this.subjects.select(".backGround")
            .attr("width", a.width + this.sobreposition ? 0 : this.getNameWidth())
            .attr("height", a.chartConfig.layout.size);

        this.subjects.select(".subject-name")
            .attr("x", 10)
            .attr("y", this.chartConfig.layout.size / 2).attr("dy", ".2em");

        this.subjects.select(".subject-tasks-g")
            .attr("transform", "translate(" + (a.sobreposition ? 0 : a.getNameWidth()) + ",0)")

        this.tasks.attr("transform", function (d) { return "translate(" + a.x(d.date.start) + ",0)" })
            .attr("width", function (d) { return a.x(d.date.end) - a.x(d.date.start) })
            .attr("height", a.y.bandwidth())
            .attr("rx", a.height / 3 > 10 ? 10 : a.height / 3)
            .attr("ry", a.height / 3 > 10 ? 10 : a.height / 3)
            .attr("stroke", "#ddd")
            .attr("stroke-width", ".5");


        return this;
    }
    getNameWidth() {
        if (this.namewidth == undefined) {
            var temp = document.querySelector("#" + this.chartConfig.name).querySelectorAll(".subject-name");
            var max = 0;
            for (var i = 0; i < temp.length; i++) {
                var temp2 = temp[i].getBoundingClientRect().width;
                var max = max > temp2 ? max : temp2;
            }
            max += 20;
            this.namewidth = max;
            return max;
        } else {
            return this.namewidth;
        }
    }
    resize(width, height) {
        var a = this;
        a.chartConfig.dimensions.width = width,
            a.chartConfig.dimensions.height = height;
        document.definewidth(a.chartConfig, 1200, a.chartConfig.layout.size * 1.1 * a.chartConfig.data.length);
        this.draw();
        return this;
    }
}
//var temp = {date:{start:"",end:"",delay:""},done:true}

document.definewidth = function (chartConfig, width, height, propWindow, propChart, target) {//prop - width/height
    if (chartConfig.dimensions == undefined) chartConfig.dimensions = {};
    chartConfig.dimensions.vertical = false;
    chartConfig.dimensions.mini = false;

    var temp;
    target = target ? target : (chartConfig.parent ? chartConfig.parent : chartConfig.target);
    if (temp = document.querySelector(target).getBoundingClientRect()) {
        chartConfig.dimensions.width = temp.width - $(target).css("padding-left").match(/[0-9]+/)[0] - $(target).css("padding-right").match(/[0-9]+/)[0] -((!chartConfig.dimensions.height && !window.mobilecheck())?13.74:0);
        console.log($(target).css("padding-right").match(/[0-9]+/)[0]);
        console.log($(target).css("padding-left").match(/[0-9]+/)[0]);
        console.log(chartConfig.dimensions.width,temp.width);
        if (propWindow) {
            var prop = window.innerWidth * propWindow / window.innerHeight;
            //console.log(prop);
            if (window.innerWidth > 991)
                chartConfig.dimensions.height = temp.width / propChart > height ? height : temp.width / propChart
            else
                chartConfig.dimensions.height = temp.width / prop, chartConfig.dimensions.vertical = prop / propWindow < 1, chartConfig.dimensions.mini = true;
        }
    } else if (chartConfig.dimensions.height == undefined)
        chartConfig.dimensions.width = width, chartConfig.dimensions.height = height;
    else
        chartConfig.dimensions.width = chartConfig.dimensions.height * propChart;

    if (chartConfig.dimensions.height == undefined)
        chartConfig.dimensions.height = !propChart || chartConfig.dimensions.width * 1 / propChart > height ? height : chartConfig.dimensions.width * 1 / propChart;
}