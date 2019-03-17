import Vue from 'vue'
import Vuex from 'vuex'
import ca from './ca'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        ca
    },
    state: {
        notifying_errors: []
    },
    mutations: {
        notify_error(state, payload) {
            state.notifying_errors.push(payload)
        },
        clear_notifications(state) {
            state.notifying_errors = []
        }
    },
    actions: {
        notify_error({ commit }, payload) {
            commit('notify_error', payload)
        },
        clear_notifications({ commit }) {
            commit('clear_notifications')
        }
    }
})
