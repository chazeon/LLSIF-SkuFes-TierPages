<template>
    <div class="ui container" id="main-container">
        <score-figure v-bind:scores="scores"></score-figure>
        <speed-figure v-bind:speeds="speeds"></speed-figure>
        <data-table
            v-bind:scores="scores"
            v-bind:speeds="speeds"
            v-bind:unit="1800"
            v-bind:interval="1"></data-table>
    </div>
</template>
<script>
import Vue from 'vue'
import VueResource from 'vue-resource'
Vue.use(VueResource)

import ScoreFigure from './components/score-figure.vue'
import SpeedFigure from './components/speed-figure.vue'
import DataTable from './components/data-table.vue'

import TierUtils from './util.js'

export default {
    props: [
        'curEventId'
    ],
    components: {
        ScoreFigure,
        SpeedFigure,
        DataTable
    },
    data: function () {
        return {
            scores: { ranks: [], time: [], records: [] },
            speeds: { ranks: [], time: [], records: [] }
        }
    },
    methods: {
        updateData: function () {
            $('.dimmer').dimmer('show')
            this.$http.get(`//api.skufes.com/tier/detail/event/${this.curEventId}/`)
            .then(response => {
                this.scores = TierUtils.groupScoreRecordByRank(response.body, 1800)
                this.speeds = TierUtils.getSpeedRecords(this.scores, 1)
            }) // Error Handling
        }
    },
    created: function () {
        this.updateData()
    },
    watch: {
        curEventId: function () {
            this.updateData()
        }
    }
}

</script>

<style>
#main-container {
    padding-top: 10px;
}
</style>