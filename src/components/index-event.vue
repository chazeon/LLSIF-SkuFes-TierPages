<template>
    <div id="main-content" class="ui vertical segment">
        <h3 class="ui header">{{currentEvent.name}}<div class="sub header">Event #{{currentEvent.event_id}}</div></h3>
        <img v-bind:src="`/static/images/event_${currentEvent.event_id}.png`" class="ui rounded image event-heading">
        <div class="ui large feed">
            <div class="event">
                <div class="label"><img v-bind:src="`/static/images/icon_framed_${currentEvent.event_id}_1.png`"></div>
                <div class="content">
                    <div class="summary">Event cutoff <a v-on:click="toggleEventTier()">{{eventCutOff.rank / 1e3}}k</a> reaches <a v-bind:href="`#/event/${currentEvent.event_id}`">{{eventCutOff.score.score.toLocaleString()}}</a><div class="date">{{fromNow(eventCutOff.time)}}</div></div>
                    <div class="extra text">up by {{eventCutOff.speed.speed.toLocaleString()}} per hour.</div>
                </div>
            </div>
            <div class="event">
                <div class="label"><img v-bind:src="`/static/images/icon_framed_${currentEvent.event_id}_2.png`"></div>
                <div class="content">
                    <div class="summary">Live cutoff <a v-on:click="toggleLiveTier()">{{liveCutOff.rank / 1e3}}k</a> reaches <a v-bind:href="`#/live/${currentEvent.event_id}`">{{liveCutOff.score.score.toLocaleString()}}</a><div class="date">{{fromNow(liveCutOff.time)}}</div></div>
                    <div class="extra text">up by {{liveCutOff.speed.speed.toLocaleString()}} per hour.</div>
                </div>
            </div>
        </div>
        <div class="ui right dividing rail">
        </div>
    </div>
</template>
<script>
import Vue from 'vue'
import VueResource from 'vue-resource'
import _ from 'lodash'
import TierUtils from './../util.js'

export default {
    props: ['currentEvent'],
    data: function () {
        return {
            currentEventData: [ { records: [ { data: [ { score: 0, time: 0, rank: 0 } ] } ], type: 'event' }, { records: [ { data: [ { score: 0, time: 0, rank: 0 } ] } ], type: 'live' } ],
            eventTierId: 0,
            liveTierId: 0,
            currentEventDetail: this.currentEvent
        }
    },
    computed: {
        eventCutOff: function () {
            let data = this.getTierData('event', this.eventTierId)
            if (data !== null) return data
            else {
                this.eventTierId = 0
                return this.getTierData('event', this.eventTierId)
            }
        },
        liveCutOff: function () {
            let data = this.getTierData('live', this.liveTierId)
            if (data !== null) return data
            else {
                this.liveTierId = 0
                return this.getTierData('live', this.liveTierId)
            }
        }
    },
    methods: {
        toggleEventTier: function () {
            let ranks = _.find(this.currentEventData, data => data.type === 'event')['ranks']
            this.eventTierId = (this.eventTierId + 1) % ranks.length
        },
        toggleLiveTier: function () {
            let ranks = _.find(this.currentEventData, data => data.type === 'live')['ranks']
            this.liveTierId = (this.liveTierId + 1) % ranks.length
        },
        getTierData: function (type, tier) {
            let records = _.find(this.currentEventData, data => data.type === type)['records']
            let data = records[tier]['data']
            let speed = ''
            if (type === 'live') speed = data && data.length > 1 ? TierUtils.calcSpeed(_.first(data), _.last(data)) : { rank: 0, time: 0, speed: '' }
            else if (type === 'event') speed = data && data.length > 1 ? TierUtils.calcSpeed(data[0], data[1]) : { rank: 0, time: 0, speed: '' }

            if (data.length > 0)
                return {
                    score: data ? data[0] : '',
                    speed: speed,
                    time: data ? new Date(data[0].time * 1e3) : Data.now(),
                    rank: data ? data[0].rank : ''
                }
            else return null
        },
        updateData: function () {
            this.$http.get(`//api.skufes.com/tier/overview/${this.currentEvent.event_id}/`)
            .then(response => {
                this.currentEventData = response.body
            })
        },
        fromNow: function (t) { return moment(t).fromNow() }
    },
    created: function () {
        this.updateData()
    }
}
</script>
<style>
#main-content {
    max-width: 540px;
}
</style>