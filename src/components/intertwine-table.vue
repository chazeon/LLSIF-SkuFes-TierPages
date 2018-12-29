<template>
    <table class="ui celled striped table dimmable">
        <thead>
            <tr>
                <th>#</th>
                <th>E1 (pt)</th>
                <th>L1 (pt/h)</th>
                <th v-if="records.ranks.length > 1">E2 (pt)</th>
                <th v-if="records.ranks.length > 1">L2 (pt)</th>
                <th v-if="records.ranks.length > 2">E3 (pt)</th>
                <th v-if="records.ranks.length > 2">L3 (pt)</th>
                <th v-if="records.ranks.length > 3">E4 (pt)</th>
                <th v-if="records.ranks.length > 3">L4 (pt)</th>
                <th v-if="records.ranks.length > 4">E5 (pt)</th>
                <th v-if="records.ranks.length > 4">L5 (pt)</th>
                <th v-if="records.ranks.length > 5">E6 (pt)</th>
                <th v-if="records.ranks.length > 5">L6 (pt)</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item_id in itemIds">
                <th>{{item_id + 1}}</th>
                <td>{{getEventScore(0, item_id)}}</td>
                <td>{{getLiveScore(0, item_id)}}</td>
                <td v-if="records.ranks.length > 1">{{getEventScore(1, item_id)}}</td>
                <td v-if="records.ranks.length > 1">{{getLiveScore(1, item_id)}}</td>
                <td v-if="records.ranks.length > 2">{{getEventScore(2, item_id)}}</td>
                <td v-if="records.ranks.length > 2">{{getLiveScore(2, item_id)}}</td>
                <td v-if="records.ranks.length > 3">{{getEventScore(3, item_id)}}</td>
                <td v-if="records.ranks.length > 3">{{getLiveScore(3, item_id)}}</td>
                <td v-if="records.ranks.length > 4">{{getEventScore(4, item_id)}}</td>
                <td v-if="records.ranks.length > 4">{{getLiveScore(4, item_id)}}</td>
                <td v-if="records.ranks.length > 5">{{getEventScore(5, item_id)}}</td>
                <td v-if="records.ranks.length > 5">{{getLiveScore(5, item_id)}}</td>
            </tr>
        </tbody>
        <!--tfoot>
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
        </tfoot-->
        <div class="ui dimmer">
            <div class="ui loader"></div>
        </div>
    </table>
</template>
<script>
import _ from 'lodash'
export default {
    props: ['records'],
    computed: {
        itemIds: function () {
            return _.range(_.max(_.map(this.records.records, records => records.data.length)))
        }
    },
    methods: {
        getEventScore: function (tierId, itemId) {
            return this.records.records[tierId].data[itemId]
            ? this.records.records[tierId].data[itemId].event.score.toLocaleString()
            : ''
        },
        getLiveScore: function (tierId, itemId) {
            return this.records.records[tierId].data[itemId]
            ? this.records.records[tierId].data[itemId].live.score.toLocaleString()
            : ''
        }
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