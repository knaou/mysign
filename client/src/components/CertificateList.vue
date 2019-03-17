<template lang="jade">
    div
        v-toolbar(v-if="adding", color="blue", dark)
            v-toolbar-title Add Certificate
            v-spacer
            v-btn(icon,@click="adding=false")
                v-icon close
        v-toolbar(v-else,color="indigo", dark)
            v-toolbar-title Certificate
            v-spacer
            v-btn(icon,@click="adding=true")
                v-icon add
        v-card
            v-data-table.elevation-1(v-if="certificates && ! adding", :headers="headers", :items="certificates")
                template(slot="items",slot-scope="props")
                    tr(@click="select(props.item)")
                        td {{ props.item.id }}
                        td {{ props.item.serial }}
                        td {{ props.item.name }}
                        td {{ props.item.description }}
                        td {{ props.item.created_at }}
                        td {{ props.item.updated_at }}
            v-card(v-else-if="adding")
                NewCertificate(:ca_id="ca_id",@added="add_cert",@close="adding=false")
        v-dialog(v-model="cert_dialog")
            Certificate(:cert="cert_dialog_cert", v-on:update:cert="update_cert", @close="cert_dialog = false")

</template>
<style scoped>
</style>
<script>
    import {mapActions} from 'vuex'
    import axios from '../../node_modules/axios'
    import NewCertificate from './NewCertificate.vue'
    import Certificate from './Certificate.vue'

    export default {
        name: "CertificateList",
        components: {NewCertificate, Certificate},
        props: ['ca_id'],
        data() {
            return {
                certificates: null,
                adding: false,
                headers: [
                    { text: 'ID', value: "id", sortable: true},
                    { text: 'serial', value: "serial", sortable: true},
                    { text: 'Name', value: "name", sortable: true},
                    { text: 'Description', value: "description", sortable: true},
                    { text: 'created_at', value: "created_at", sortable: true },
                    { text: 'updated_at', value: "updated_at", sortable: true }
                ],
                cert_dialog: false,
                cert_dialog_cert: null
            }
        },
        watch: {
            ca_id(id) {
                this.update_from_ca(id);
            }
        },
        mounted() {
            this.update_from_ca(this.ca_id);
        },
        methods: {
            update_from_ca(id) {
                this.certificates = null;
                axios.get(`/api/certificate_authoritys/${id}/certificates/`).then(res => {
                    this.$set(this, 'certificates', res.data);
                }).catch(function(err){
                    this.notify_error(err.message);
                });
            },
            add_cert(cert) {
                this.certificates.push(cert);
            },
            select(item) {
                this.cert_dialog_cert = item;
                this.cert_dialog = true;
            },
            update_cert(item) {
                this.certificates.filter(e => e.id === item.id).forEach((v, i) => {
                    this.$set(this.certificates, i, item);
                });
                this.cert_dialog_cert = item;
            },
            ...mapActions(['notify_error'])
        }
    }
</script>
