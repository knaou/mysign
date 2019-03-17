<template lang="jade">
    v-app#inspire
        v-toolbar(color="blue darken-3",dark,app,fixed)
            v-toolbar-title.ml-0.pl-3(style="width: 300px")
                span.hidden-sm-and-down Mysign
        Home
        v-snackbar(v-model="notifying_errors.length > 0",:top="true",:auto-height="true",:timeout="0",:vertical="true")
          v-btn(color="pink",flat,@click="clear_notifications") Close
          div(v-for="err in notifying_errors", :key="err")
            v-alert(:value="true", type="error") {{err}}

</template>

<script>
    import {mapState, mapActions} from 'vuex';
    import Home from './components/Home.vue';

    export default {
        name: 'App',
        components: {Home},
        computed: {
            ...mapState(['notifying_errors'])
        },
        methods: {
            ...mapActions([
                'notify_error',
                'clear_notifications'
            ])
        }
    }
</script>

