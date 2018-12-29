<template>
    <div class="dimmable">
        <div id="plot">
        </div>
        <div class="ui dimmer">
            <div class="ui loader"></div>
        </div>
    </div>
</template>
<script>
import Vue from 'vue'

export default {
    props: ['records', 'ylabel', 'property'],
    mounted: function () {
    },
    methods: {
        getLayout: function () {
            return {
                xaxis: {
                    rangeselector: {
                        buttons: []
                    },
                },
                yaxis: { title: this.ylabel },
                font: { family: 'Lato' },
                margin: { t: 0, b: 22, l: 50, r: 0 },
                height: 250,
                legend: {"orientation": "h"}
            }
        },
        plotlyPlot: function (records) {
            let datasets = _.values(_.mapValues(records.records, tierRecords => {
                return {
                    x: _.map(tierRecords.data, record => new Date(record['time'] * 1e3)),
                    y: _.map(tierRecords.data, record => record[this.property]),
                    type: 'line',
                    name: parseInt(tierRecords.rank).toLocaleString(),
                }
            }))
            Plotly.purge(this.$el.childNodes[0])
            Plotly.newPlot(this.$el.childNodes[0], _.values(datasets), this.getLayout(), { displaylogo: false })
            this.$el.childNodes[0].on('plotly_afterplot', () => {
                if (datasets.length > 0) $(this.$el).dimmer('hide')
            });
        }
    },
    watch: {
        records: function (records) {
            this.plotlyPlot(records)
            /*
            if (records.time.length > 0) {
                $(this.$el.childNodes[0]).dimmer('hide')
            } else {
                $(this.$el.childNodes[0]).dimmer('show')
            }
            */
        }
    },
    mounted: function () {
        $(this.$el).dimmer('show')
        //this.plotlyPlot(this.records)
        $(window).on("resize", () => {
            //console.log(this.$el.childNodes[0])
            Plotly.Plots.resize(this.$el.childNodes[0], {
                width: $(this.$el).width()
            })
        })
    },
    beforeDestroy: function () {
        Plotly.purge(this.$el.childNodes[0])
    }
}
</script>
<style>
#plot {
    height: 250px
}
</style>