<template lang="jade">
    v-content
        v-container(fluid)
            v-layout(row,justify-space-between)
                v-flex(xs3)
                    .menu
                        v-treeview(:active.sync="tree",:items="items", item-key="key", activatable, open-on-click)
                            v-icon(v-if="item.icon",slot="prepend",slot-scope="{ item, open }") {{item.icon}}
                v-flex(xs9,v-if="page=='__new_ca__'")
                    v-card
                        NewCA
                v-flex(xs9,v-else-if="selected_ca")
                    CA(:ca="selected_ca")
                v-flex(xs9,v-else)
                    p Welcome to MySign !!!

</template>

<script>
    import { mapState, mapActions } from 'vuex'
    import NewCA from './NewCA.vue'
    import CA from './CA.vue'

    export default {
        name: "Home",
        components: { NewCA, CA },
        data() {
            return {
                initialized: false,
                selected_tree: []
            }
        },
        computed: {
            tree: {
                get()  {
                    if(this.selected_ca) {
                        return [`ca_${this.selected_ca.id}`]
                    } else {
                        return this.selected_tree;
                    }
                },
                set(v) {
                    this.selected_tree = v;
                    if (v && v.length > 0 && v[0].startsWith('ca_')) {
                        let id = parseInt(v[0].slice('ca_'.length));
                        this.request_ca_by_id(id);
                    } else {
                        this.request_ca_by_id(null);
                    }
                }
            },
            page() {
                return this.tree.length === 0 ? null : this.tree[0];
            },
            items() {
                var cas = [];
                var index = 0;

                this.$set(cas, index++, {
                    key: 'home',
                    name: 'Hoome',
                    icon: 'home'
                });

                this.ca_list.forEach( ca => {
                    this.$set(cas, index++, {
                        icon: 'note',
                        key: 'ca_' + ca.id,
                        name: ca.name,
                        ca_id: ca.id
                    })
                });

                this.$set(cas, index++, {
                    icon: 'note_add',
                    key: '__new_ca__',
                    name:'New CA'
                });

                return cas;
            },
            ...mapState('ca', ['ca_list', 'selected_ca'])
        },
        mounted() {
            this.initialized = false;
            this.request_ca_list({}).then(() => this.initialized = true);
        },
        methods: {
            ...mapActions('ca', ['request_ca_list', 'request_ca_by_id'])
        }
    }
</script>

<style scoped>
    .menu {
        padding: 0em 1em;
    }
</style>
