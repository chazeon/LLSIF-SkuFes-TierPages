import Vue              from 'vue'
import VueRouter        from 'vue-router'

import IndexApp         from './index.vue'
import EventScoreApp    from './event-score.vue'
import LiveScoreApp     from './live-score.vue'
import IntertwineApp     from './intertwine.vue'

import EventSelector    from './event-selector.vue'

import _ from 'lodash'
import events from './events.js'

Vue.use(VueRouter)

const routes = [
    { path: '/', component: IndexApp },
    { path: '/event/:curEventId', component: EventScoreApp, props: true },
    { path: '/live/:curEventId', component: LiveScoreApp, props: true },
    { path: '/intertwine/:curEventId', component: IntertwineApp, props: true },
]

const router = new VueRouter({
    routes,
    linkActiveClass: 'active'
})

Vue.component('event-selector', EventSelector)

const app = new Vue({
    router,
    data: {
        curEventId: events.EVENT_ID_DEFAULT,
    },
    components: [
        EventSelector
    ],
    watch: {
        curEventId: function () {
            router.replace(router.currentRoute.path.replace(/\/\d+$/, `/${this.curEventId}`))
        }
    },
    updated: function () {
        //let curEventId = parseInt(router.currentRoute.params['curEventId'])
        //this.curEventId = !isNaN(curEventId) ? curEventId : events.EVENT_ID_DEFAULT
    }
}).$mount('#app')