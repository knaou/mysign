<template lang="jade">
    div
        v-toolbar(color="indigo", dark)
            v-toolbar-title(v-if="cert") {{cert.name}}
            v-spacer
            v-btn(icon,@click="close")
                v-icon close
        v-card
            v-container(fluid,grid-list-lg)
                v-layout(row,wrap)
                    v-flex(xs12)
                        v-toolbar(v-if="editing",color="blue", dark)
                            v-toolbar-title Edit Basic Info.
                            v-spacer
                            v-btn(icon,@click="edit_view(false)")
                                v-icon close
                        v-toolbar(v-else,color="indigo", dark)
                            v-toolbar-title Basic Info.
                            v-spacer
                            v-btn(icon,@click="edit_view(true)")
                                v-icon edit
                        v-card
                            v-container(v-if="editing")
                                form(@submit.prevent="update_cert_by_new_cert")
                                    v-layout(row,wrap)
                                        v-flex(xs12)
                                            v-text-field(prepend-icon="folder_open",label="Name",v-model="new_cert.name")
                                        v-flex(xs12)
                                            v-textarea(prepend-icon="info",auto-grow,label="Description",v-model="new_cert.description")
                                        v-flex(xs12)
                                    v-btn(color="primary", @click="update_cert_by_new_cert") Submit
                            v-container(v-else-if="cert")
                                v-layout(row,wrap)
                                    v-flex(xs12)
                                        v-text-field(prepend-icon="folder_open",readonly,label="Name",v-model="cert.name")
                                    v-flex(xs12)
                                        v-textarea(prepend-icon="info",readonly,auto-grow,label="Description",v-model="cert.description")
                    v-flex(xs12,v-if="cert")
                        v-toolbar(color="indigo", dark)
                            v-toolbar-title Onther Information
                        v-card
                            v-container
                                v-text-field(readonly,label="ID",v-model="cert.id")
                                v-text-field(readonly,label="Created At",v-model="cert.created_at")
                                v-text-field(readonly,label="Updated At",v-model="cert.updated_at")
                                a(:href="`/api/certificates/${cert.id}/keyfile`")
                                    v-btn(color="info")
                                        | Key
                                        v-icon(right) cloud_download
                                a(:href="`/api/certificates/${cert.id}/csrfile`")
                                    v-btn(color="info")
                                        | CSR
                                        v-icon(right) cloud_download
                                a(:href="`/api/certificates/${cert.id}/certfile`")
                                    v-btn(color="info")
                                        | Cert
                                        v-icon(right) cloud_download
</template>
<style scoped>
</style>
<script>
    import {mapActions} from 'vuex';
    import axios from '../../node_modules/axios'

    export default {
        name: "Certificate",
        props: ['cert'],
        data() {
            return {
                editing: false,
                new_cert: null
            }
        },
        methods: {
            close() {
                this.$emit('close')
            },
            edit_view(open) {
                if(open){
                    this.new_cert = Object.assign({},this.cert);
                }
                this.editing = open;
            },
            update_cert_by_new_cert() {
                axios.put(`/api/certificates/${this.new_cert.id}/`, this.new_cert).then(res => {
                    this.$emit('update:cert', res.data);
                    this.edit_view(false)
                }).catch(err => {
                    notify_error(err.message);
                    console.log(err);
                })
            },
            ...mapActions(['notify_error'])
        }
    }
</script>
