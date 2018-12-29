<template>
    <div class="ui vertical fluid segment">
        <h5 class="ui header">Speed Plot</h5>
        <figure-template
            v-bind:records="speeds"
            v-bind:ylabel="'Speed (pt/h)'"
            v-bind:property="'speed'"></figure-template>
    </div>
</template>
<script>
import Vue from 'vue'
import FigureTemplate from './figure-template.vue'
export default {
    props: [ "speeds" ],
    components: {
        FigureTemplate
    }
}
</script>