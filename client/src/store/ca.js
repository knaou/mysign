import axios from '../../node_modules/axios'

export default {
    namespaced: true,
    state: {
        selected_ca: null,
        ca_list: [],
        ca_list_requesting: false
    },
    mutations: {
        set_ca_list_requesting(state, payload) {
            state.ca_list_requesting = payload
        },
        add_ca (state, payload) {
            state.ca_list.push(payload)
        },
        set_ca_list (state, payload) {
            state.ca_list = payload
        },
        update_ca_with(state, payload) {
            state.ca_list.forEach(ca => {
                if(ca.id == payload.id){
                    Object.keys(payload).forEach(key => {
                        ca[key] = payload[key]
                    })
                }
                state.selected_ca = payload
            })
        },
        select_ca(state, payload) {
            state.selected_ca = payload
        }
    },
    actions: {
        add_ca ({commit}, payload) {
            commit('add_ca', payload)
        },
        select_ca({commit}, payload) {
            commit('select_ca', payload);
        },
        async update_ca_with({ commit }, payload) {
            let id = payload.id
            let res = await axios.put(`/api/certificate_authoritys/${id}/`, payload).catch(function(err){
                commit('notify_error', err.message, { root: true });
                console.log(err);
                return null;
            });
            if (res) {
                commit('update_ca_with', res.data);
                commit('select_ca', res.data);
            }
        },
        async request_ca_by_id({commit}, payload) {
            if (payload) {
                let res = await axios.get(`/api/certificate_authoritys/${payload}/`).catch(err => {
                    commit('notify_error', err.message, { root: true });
                    console.log(err);
                    return null;
                });
                if (res) commit('select_ca', res.data);
            } else {
                commit('select_ca', null);
            }
        },
        async request_ca_list({ commit, dispatch }, payload){
            commit('set_ca_list_requesting', true)
            let res = await axios.get('/api/certificate_authoritys/').catch(err => {
                commit('set_ca_list_requesting', false);
                commit('notify_error', err.message, { root: true });
                console.log(err);
                return null;
            });
            commit('set_ca_list_requesting', false);
            if (res) commit('set_ca_list', res.data);

            if(payload && payload.selected_ca_id) {
                await dispatch('request_ca_by_id', payload.selected_ca_id);
            }
        }
    }
}
