import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify)

import App from './App.vue'
import store from './store'

require('./index.html');
require('./common.less');

//Vue.config.productionTip = false

new Vue({
    el: '#app',
    store,
    components: {App},
    template: '<App/>'
});
