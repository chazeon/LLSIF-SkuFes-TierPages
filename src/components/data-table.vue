<template>
    <table class="ui celled striped table dimmable">
        <thead>
            <tr>
                <th>Time</th>
                <th>T1 (pt)</th>
                <th>V1 (pt/h)</th>
                <th v-if="scores.ranks.length > 1">T2 (pt)</th>
                <th v-if="scores.ranks.length > 1">V2 (pt/h)</th>
                <th v-if="scores.ranks.length > 2">T3 (pt)</th>
                <th v-if="scores.ranks.length > 2">V3 (pt/h)</th>
                <th v-if="scores.ranks.length > 3">T4 (pt)</th>
                <th v-if="scores.ranks.length > 3">V4 (pt/h)</th>
                <th v-if="scores.ranks.length > 4">T5 (pt)</th>
                <th v-if="scores.ranks.length > 4">V5 (pt/h)</th>
                <th v-if="scores.ranks.length > 5">T6 (pt)</th>
                <th v-if="scores.ranks.length > 5">V6 (pt/h)</th>
            </tr>
        </thead>
        <paginate name="times" v-bind:list="scores.time" v-bind:per="20" tag="tbody">
            <tr v-for="t in paginated('times')">
                <td>{{getTime(t)}}</td>
                <td>{{getScore(t, 0, unit)}}</td>
                <td>{{getSpeed(t, 0, unit)}}</td>
                <td v-if="scores.ranks.length > 1">{{getScore(t, 1, unit)}}</td>
                <td v-if="scores.ranks.length > 1">{{getSpeed(t, 1, unit)}}</td>
                <td v-if="scores.ranks.length > 2">{{getScore(t, 2, unit)}}</td>
                <td v-if="scores.ranks.length > 2">{{getSpeed(t, 2, unit)}}</td>
                <td v-if="scores.ranks.length > 3">{{getScore(t, 3, unit)}}</td>
                <td v-if="scores.ranks.length > 3">{{getSpeed(t, 3, unit)}}</td>
                <td v-if="scores.ranks.length > 4">{{getScore(t, 4, unit)}}</td>
                <td v-if="scores.ranks.length > 4">{{getSpeed(t, 4, unit)}}</td>
                <td v-if="scores.ranks.length > 5">{{getScore(t, 5, unit)}}</td>
                <td v-if="scores.ranks.length > 5">{{getSpeed(t, 5, unit)}}</td>
            </tr>
        </paginate>
        <tfoot>
            <th v-bind:colspan="scores.ranks.length * 2 + 1">
                <paginate-links
                    for="times"
                    v-bind:limit="5"
                    class="ui right floated pagination menu"
                    v-bind:classes="{
                        'a': 'item'
                    }"
                    container-tag="div"
                    item-tag="a"
                    link-tag="span"
                    click-handler-tag="item"></paginate-links>
            </th>
        </tfoot>
        <div class="ui dimmer">
            <div class="ui loader"></div>
        </div>
    </table>
</template>
<script>
import Vue from 'vue'
import VuePaginate from '../plugins/vue-paginate'
Vue.use(VuePaginate)

import _ from 'lodash'

export default {
    props: [
        'scores', 'speeds', 'unit', 'interval'
    ],
    methods: {
        getTime: function (t) {
            return moment(new Date((t / this.unit | 0) * this.unit * 1000)).format('MM-DD HH:mm')
        },
        getRecordId: function (time, floor, records) {
            return _.findIndex(records.data, record => {
                return (record.time / floor | 0) === (time / floor | 0)
            })
        },
        getScore: function (time, rankId, floor) {
            let rank = this.scores.ranks[rankId]
            if (rank === undefined) return ''
            let recordGroupId = _.findIndex(this.scores.records, record => record.rank === rank)
            let recordId = this.getRecordId(time, floor, this.scores.records[recordGroupId])
            if (recordId === -1) return ''
            return this.scores.records[recordGroupId]['data'][recordId]['score'].toLocaleString()
        },
        getSpeed: function (time, rankId, floor) {
            let rank = this.speeds.ranks[rankId]
            if (rank === undefined) return ''
            let recordGroupId = _.findIndex(this.speeds.records, record => record.rank === rank)
            let recordId = this.getRecordId(time, floor, this.speeds.records[recordGroupId])
            if (recordId === -1) return ''
            return this.speeds.records[recordGroupId]['data'][recordId]['speed'].toLocaleString()
        },
    },
    data: function () {
        return {
            paginate: ['times']
        }
    },
    watch: {
        scores: function (scores) {
            if (scores.time.length > 0) {
                $(this.$el).dimmer('hide')
            } else {
                $(this.$el).dimmer('show')
            }
        }
    },
    mounted: function () {
        $(this.$el).dimmer('show')
    }
}
</script>
<style>
    ul.paginate-links {
        padding: 0;
    }
    ul.paginate-links > li {
        list-style: none;
    }
    ul.paginate-links > li.active > a.item {
        border-top: none;
        background-color: rgba(0,0,0,.05);
        color: rgba(0,0,0,.95);
        box-shadow: none;
    }
</style>