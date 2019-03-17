<template lang="jade">
    div
        div(v-if="ca")
            v-container(fluid,grid-list-lg)
                v-layout(row,wrap)
                    v-flex(xs12)
                        v-toolbar(v-if="editing",color="blue", dark)
                            v-toolbar-title Edit Basic info.
                            v-spacer
                            v-btn(icon,@click="edit_view(false)")
                                v-icon close
                        v-toolbar(v-else,color="indigo", dark)
                            v-toolbar-title Basic info.
                            v-spacer
                            v-btn(icon,@click="edit_view(true)")
                                v-icon edit
                        v-card
                            v-container(v-if="editing")
                                form(@submit.prevent="update_ca_by_new_ca")
                                    v-layout(row,wrap)
                                        v-flex(xs12)
                                            v-text-field(prepend-icon="folder_open",label="Name",v-model="new_ca.name")
                                        v-flex(xs12)
                                            v-textarea(prepend-icon="info",auto-grow,label="Description",v-model="new_ca.description")
                                        v-flex(xs12)
                                    v-btn(color="primary", @click="update_ca_by_new_ca") Submit
                            v-container(v-else)
                                v-layout(row,wrap)
                                    v-flex(xs12)
                                        v-text-field(prepend-icon="folder_open",readonly,label="Name",v-model="ca.name")
                                    v-flex(xs12)
                                        v-textarea(prepend-icon="info",readonly,auto-grow,label="Description",v-model="ca.description")
                    v-flex(xs12)
                        CertificateList(:ca_id="ca.id")
                    v-flex(xs12)
                        v-toolbar(color="indigo", dark)
                            v-toolbar-title Other Information
                        v-card
                            v-container
                                v-text-field(readonly,label="ID",v-model="ca.id")
                                v-text-field(readonly,label="Next Serial",v-model="ca.next_serial")
                                v-text-field(readonly,label="Created At",v-model="ca.created_at")
                                v-text-field(readonly,label="Updated At",v-model="ca.updated_at")
                                a(:href="`/api/certificate_authoritys/${ca.id}/keyfile`")
                                    v-btn(color="info")
                                        | Key
                                        v-icon(right) cloud_download
                                a(:href="`/api/certificate_authoritys/${ca.id}/csrfile`")
                                    v-btn(color="info")
                                        | CSR
                                        v-icon(right) cloud_download
                                a(:href="`/api/certificate_authoritys/${ca.id}/certfile`")
                                    v-btn(color="info")
                                        | Cert
                                        v-icon(right) cloud_download
        div(v-else)
            p requesting...
</template>
<style scoped>
</style>
<script>
    import {mapActions} from 'vuex'
    import CertificateList from './CertificateList.vue'

    export default {
        name: "CA",
        components: {CertificateList},
        props: ['ca'],
        data() {
            return {
                editing: false,
                new_ca: null
            }
        },
        methods: {
            edit_view(open) {
                if (open){
                    this.new_ca = Object.assign({},this.ca);
                }
                this.editing = open;
            },
            update_ca_by_new_ca() {
                this.ca = this.new_ca;
                this.update_ca_with(this.new_ca);
                this.editing = false;
            },
            ...mapActions('ca', ['update_ca_with']),
            ...mapActions(['notify_error'])
        }
    }
</script>
