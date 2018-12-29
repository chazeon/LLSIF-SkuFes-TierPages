<template>
    <div class="right menu">
        <div class="ui dropdown item" lang="jp" id="event-select-dropdown">
            #{{ curEvent.event_id }}: {{ curEvent.name }}
            <i class="dropdown icon"></i>
            <div class="ui menu">
                <div class="item" v-for="event in events" v-on:click="updateCurEventId(event.event_id)">#{{event.event_id}}: {{event.name}}</div>
            </div>
        </div>
   </div>
</template>
<script>
import Vue from 'vue'
import VueResource from 'vue-resource'
import _ from 'lodash'
import events from './events.js'

export default {
    props: [ 'curEventId' ],
    data: function () {
        return {
            events: events.events
        }
    },
    methods: {
        updateCurEventId: function (newCurEventId) {
            this.$emit('update:cur-event-id', newCurEventId)
        },
        toggleMenu: function () {
            $('#event-select-dropdown').dropdown('show')
        }
    },
    computed: {
        curEvent: function () {
            let curEventId = this.curEventId
            return _.find(this.events, event => event.event_id === curEventId)
        }
    },
    mounted: function () {
        $('#event-select-dropdown').dropdown()
    },
    created: function () {
        this.$http.get('//api.skufes.com/db/event/')
        .then(response => {
            this.events = response.body.filter(event => event.event_id > 96).sort((event_a, event_b) => event_b.event_id - event_a.event_id)
            this.updateCurEventId(this.events[0].event_id)
        })
    }
}
</script>
<style>
#event-select-dropdown > .menu {
    z-index: 2000
}
</style>