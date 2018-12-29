<template>
    <div class="ui vertical fluid segment">
        <h5 class="ui header">Score Plot</h5>
        <figure-template
            v-bind:records="scores"
            v-bind:ylabel="'Score (pt)'"
            v-bind:property="'score'"></figure-template>
    </div>
</template>
<script>
import Vue from 'vue'
import FigureTemplate from './figure-template.vue'
export default {
    props: [ "scores" ],
    components: {
        FigureTemplate
    }
}
</script>