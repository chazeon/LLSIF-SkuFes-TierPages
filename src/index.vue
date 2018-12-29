<template>
<div class="ui container" id="main-container">
    <paginate name="events" v-bind:list="events" v-bind:per="10" tag="div" class="ui container">
        <index-event v-for="event in paginated('events')" v-bind:currentEvent="event" v-bind:key="event.event_id"></index-event>
    </paginate>
    <paginate-links for="events" v-bind:limit="5"  class="ui pagination menu" v-bind:classes="{ 'a': 'item' }" v-bind:hide-single-page="true"></paginate-links>
</div>
</template>
<script>
import Vue from 'vue'
import VuePaginate from 'vue-paginate'
import IndexEvent from './components/index-event.vue'
import events from './events.js'

Vue.component('index-event', IndexEvent)
Vue.use(VuePaginate)

export default {
    data: function () {
        return {
            events: events.events,
            paginate: ['events']
        }
    },
    created: function () {
        this.$http.get('//api.skufes.com/db/event/')
        .then(response => {
            this.events = response.body.filter(event => event.event_id > 96).sort((event_a, event_b) => event_b.event_id - event_a.event_id)
        })
    }
}
</script>
<style>
#main-container {
    margin-top: 5px;
    margin-bottom: 5px;
}
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