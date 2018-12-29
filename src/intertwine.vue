<template>
<div class="ui container" id="main-container">
    <div class="ui vertical fluid segment">
        <h5 class="ui header">Intertwine Plot</h5>
        <intertwine-figure :records="dataset"></intertwine-figure>
        <intertwine-table :records="dataset"></intertwine-table>
    </div>
</div>
</template>
<script>

import Vue from 'vue'
import VueResource from 'vue-resource'
Vue.use(VueResource)

import IntertwineFigure from './components/intertwine-figure.vue'
Vue.component('intertwine-figure', IntertwineFigure)

import IntertwineTable from './components/intertwine-table.vue'
Vue.component('intertwine-table', IntertwineTable)

//import ScoreFigure from './components/score-figure.vue'
//import SpeedFigure from './components/speed-figure.vue'
//import DataTable from './components/data-table.vue'

import TierUtils from './util.js'
import _ from 'lodash'

export default {
    props: [
        'curEventId'
    ],
    data: function () {
        return {
            raw: {
                live: { ranks: [], time: [], records: [] },
                event: { ranks: [], time: [], records: [] }
            },
            dataset: {
                ranks: [],
                records: []
            },
            needUpdate: 0
        }
    },
    computed: {
    },
    created: function () {
        this.updateData()
    },
    methods: {
        updateData: function () {
            $('.dimmer').dimmer('show')
            this.$http.get(`//api.skufes.com/tier/detail/event/${this.curEventId}/`)
            .then(response => {
                this.raw.event = TierUtils.groupScoreRecordByRankForce(response.body, 1800)
                this.needUpdate += 1
            })
            this.$http.get(`//api.skufes.com/tier/detail/live/${this.curEventId}/`)
            .then(response => {
                this.raw.live = TierUtils.groupScoreRecordByRankForce(response.body, 1800)
                this.needUpdate += 1
            })
        },

        updateDataset: function () {
            let ranks = [], records = [], times = []
            for (let eventRankId = 0; eventRankId < this.raw.event.ranks.length; ++eventRankId) {
                let rankRecords = []
                let currRank = this.raw.event.ranks[eventRankId]
                let liveRankId = this.raw.live.ranks.indexOf(currRank)
                if (this.raw.live.records[liveRankId] === undefined
                || this.raw.event.records[eventRankId] === undefined)
                    continue
                let liveRecords = this.raw.live.records[liveRankId].data
                let eventRecords = this.raw.event.records[eventRankId].data
                for (let eventRecord of eventRecords) {
                    let liveRecord = _.sortBy(liveRecords, liveRecord => Math.abs(eventRecord.time - liveRecord.time) )[0]
                    rankRecords.push({ event: eventRecord, live: liveRecord })
                }
                ranks.push(currRank)
                records.push({ data: rankRecords, rank: currRank })
            }
            this.dataset = { ranks, records }
        }
    },
    watch: {
        needUpdate: function (needUpdate) {
            if (needUpdate > 1 && this.raw.live.records.length > 0 && this.raw.event.records.length > 0) {
                this.updateDataset()
                this.needUpdate = 0
            }
        },
        curEventId: function () {
            this.updateData()
        }
    }
}
</script>

<style>
#main-container {
    padding-top: 10px;
    padding-bottom: 10px;
}
</style>