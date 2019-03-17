<template lang="jade">
    v-stepper(v-model="step",vertical)
        // Step 1
        v-stepper-step(:complete="step > 1",step="1") Fulfill Basic Info.
        v-stepper-content(step="1")
            v-card.mb-2
                v-layout(row,wrap)
                    v-flex(xs12,align-center,justify-space-between)
                        v-text-field(prepend-icon="folder_open",label="Name",v-model="req.name")
                    v-flex(xs12)
                        v-textarea(prepend-icon="info",label="Description",v-model="req.description")
            v-btn(color="primary",@click="next") Next
        // Step 2
        v-stepper-step(:complete="step > 2",step="2") Create PrivateKey
        v-stepper-content(step="2")
            v-card.mb-2
                v-layout(row,wrap)
                    v-flex(xs12)
                        v-radio-group(v-model="req.private_key")
                            v-radio(label="Create",value="create")
                            v-radio(label="From PEM",value="input")
                    v-flex(xs12,v-show="req.private_key=='input'")
                        v-textarea(v-model="req.private_key_pem",prepend-icon="business",label="Private Key")
            v-btn(color="primary",@click="next") Next
            v-btn(flat,@click="step = 1") Prev
        // Step 3
        v-stepper-step(:complete="step > 3",step="3") Create Request
        v-stepper-content(step="3")
            v-card.mb-2
                v-layout(row,wrap)
                    v-flex(xs12)
                        v-radio-group(v-model="req.csr")
                            v-radio(label="CSR",value="create")
                            v-radio(label="From PEM",value="input")
                    v-flex(xs6,v-show="req.csr=='create'")
                        v-text-field(v-model="req.csr_C",prepend-icon="business",label="Country Name")
                    v-flex(xs6,v-show="req.csr=='create'")
                        v-text-field(v-model="req.csr_ST",prepend-icon="business",label="State Or Province Name")
                    v-flex(xs6,v-show="req.csr=='create'")
                        v-text-field(v-model="req.csr_L",prepend-icon="business",label="Locality Name")
                    v-flex(xs6,v-show="req.csr=='create'")
                        v-text-field(v-model="req.csr_O",prepend-icon="business",label="Organization Name")
                    v-flex(xs6,v-show="req.csr=='create'")
                        v-text-field(v-model="req.csr_OU",prepend-icon="business",label="Organizational Unit Name")
                    v-flex(xs6,v-show="req.csr=='create'")
                        v-text-field(v-model="req.csr_CN",prepend-icon="business",label="Common Name")
                    v-flex(xs12,v-show="req.csr=='create'")
                        v-text-field(v-model="req.csr_emailAddress",prepend-icon="mail",label="EMail Address")
                    v-flex(xs12,v-show="req.csr=='input'")
                        v-textarea(v-model="req.csr_pem",prepend-icon="business", label="CSR",box)
            v-btn(color="primary",@click="next") Submit
            v-btn(flat,@click="step = 2") Prev
        // Step 4
        v-stepper-step(:complete="step > 4",step="4") Submitted
        v-stepper-content(step="4")
            v-progress-circular(v-if="requesting && !error",indeterminate,color="primary")
            v-alert(:value="success",type="success") Success!
            v-btn(v-if="success", color="primary",@click="close_and_move") Open

            v-btn(v-if="success",@click="reset(true)") Create Another One
            v-alert(:value="error",type="error")
                p Oops, failed
                p {{error}}
            v-btn(v-if="error",@click="reset(false)") Restart
</template>

<script>
    import { mapActions } from 'vuex'
    import axios from '../../node_modules/axios'

    export default {
        name: "NewCA",
        data() {
            return {
                req: {},
                requesting: false,
                error: null,
                success: false,
                step: 1,
                result: null
            }
        },
        mounted() {
          this.reset(true)
        },
        methods: {
            reset(reset_value) {
                if (reset_value) {
                    this.req = {
                        name: 'Name',
                        description: 'Description',
                        private_key: 'create',
                        private_key_pem: '',
                        csr: 'create',
                        csr_C: 'JP',
                        csr_ST: 'State',
                        csr_L: 'local',
                        csr_O: 'Organization Name',
                        csr_OU: 'Organizational Unit Name',
                        csr_CN: 'example.com',
                        csr_emailAddress: 'sitemaster@example.com',
                        csr_pem: ''
                    }
                }
                this.step = 1;
                this.requesting = false;
                this.error = null;
                this.success = false;
            },
            next(){
                this.step += 1;
                if(this.step === 4) {
                    this.submit();
                }
            },
            close_and_move() {
                this.select_ca(this.result)
            },
            submit() {
                this.requesting = true;
                axios.post('/api/certificate_authoritys/wizard/', this.req).then(req => {
                    this.add_ca(req.data);
                    this.result = req.data;
                    this.requesting = false;
                    this.success = true;
                }).catch(err=>{
                    this.error = err.response.data;
                })
            },
            ...mapActions(['notify_error']),
            ...mapActions('ca', ['add_ca', 'request_ca_by_id', 'select_ca'])
        }
    }
</script>

<style scoped>

</style>
