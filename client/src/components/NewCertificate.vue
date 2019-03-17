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
        v-stepper-step(:complete="step > 3",step="3") Create CSR
        v-stepper-content(step="3")
            v-card.mb-2
                v-layout(row,wrap)
                    v-flex(xs12)
                        v-radio-group(v-model="req.csr")
                            v-radio(label="Create",value="create")
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
                        v-textarea(v-model="req.csr_pem",prepend-icon="business", label="CSR")
            v-btn(color="primary",@click="next") Next
            v-btn(flat,@click="step = 2") Prev
            // Step 4
        v-stepper-step(:complete="step > 4",step="4") Additional Info.
        v-stepper-content(step="4")
            v-card.mb-2
                v-layout(row,wrap)
                    v-flex(xs12)
                        v-text-field(v-model="req.sans",prepend-icon="business",label="Subject Alternative Name", placeholder="DNS:hoge.example.com, IP:192.168.0.1")
                    v-flex(xs6)
                        p Usage
                        v-checkbox(v-model="req.usages", value="digital_signature",label="Digital Signature")
                        v-checkbox(v-model="req.usages", value="non_repudiation",label="Non Repudiation")
                        v-checkbox(v-model="req.usages", value="key_encipherment",label="Key Encipherment")
                        v-checkbox(v-model="req.usages", value="data_encipherment",label="Data Encipherment")
                        v-checkbox(v-model="req.usages", value="key_agreement",label="Key Aggrement")
                        v-checkbox(v-model="req.usages", value="key_cert_sign",label="Key Cert Sign")
                        v-checkbox(v-model="req.usages", value="crl_sign",label="CRL Sign")
                        v-checkbox(v-model="req.usages", value="encipher_only",label="Encipher Only")
                        v-checkbox(v-model="req.usages", value="decipher_only",label="Decipher Only")
                    v-flex(xs6)
                        p Extendted Usage
                        v-checkbox(v-model="req.ext_usages", value="server_auth",label="TLS Web Server Auth.")
                        v-checkbox(v-model="req.ext_usages", value="client_auth",label="TLS Web Client Auth.")
                        v-checkbox(v-model="req.ext_usages", value="code_signing",label="Code Signing")
                        v-checkbox(v-model="req.ext_usages", value="email_protection",label="Email Protection(e.g. S/MIME)")
                        v-checkbox(v-model="req.ext_usages", value="time_stamping",label="Timestamp")
                        v-checkbox(v-model="req.ext_usages", value="ms_sgc",label="Microsoft Server Gated Crypto")
                        v-checkbox(v-model="req.ext_usages", value="ns_sgc",label="Netscape Server Gated Crypto")
                        v-checkbox(v-model="req.ext_usages", value="ms_smartcard_login",label="Microsoft Smartcardlogin")

            v-btn(color="primary",@click="next") Submit
            v-btn(flat,@click="step = 3") Prev
        // Step 5
        v-stepper-step(:complete="step > 5",step="5") Submitted
        v-stepper-content(step="5")
            v-progress-circular(v-if="requesting && !error",indeterminate,color="primary")

            v-alert(:value="success",type="success") Success!
            v-btn(v-if="success", color="primary", @click="close") Close
            v-btn(v-if="success",@click="reset(true)") Create Another One

            v-alert(:value="error",type="error")
                p Oops, Failed
                p {{error}}
            v-btn(v-if="error", color="primary",@click="reset(false)") Restart
            v-btn(v-if="error", @click="close") Close

</template>

<script>
    import { mapActions } from 'vuex'
    import axios from '../../node_modules/axios'

    export default {
        name: "NewCertificate",
        props: ['ca_id'],
        data() {
            return {
                req: {},
                requesting: false,
                error: null,
                success: false,
                step: 1
            }
        },
        mounted() {
          this.reset(true);
        },
        methods: {
            reset(reset_value) {
                if (reset_value) {
                    this.req = {
                        name: 'Name',
                        description: '',
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
                        csr_pem: '',
                        sans: '',
                        usages: ['digital_signature', 'non_repudiation', 'key_encipherment', 'data_encipherment', 'key_agreement', 'key_cert_sign'],
                        ext_usages: ['server_auth', 'client_auth', 'code_signing', 'email_protection']
                    }
                }
                this.step = 1;
                this.requesting = false;
                this.error = null;
                this.success = false;
            },
            next(){
                this.step += 1;
                if(this.step === 5) {
                    this.submit();
                }
            },
            submit() {
                this.requesting = true;
                let self = this;
                axios.post(`/api/certificate_authoritys/${this.ca_id}/certificates/`, this.req).then(req => {
                    self.$emit('added', req.data);
                    self.requesting = false;
                    self.success = true;
                }).catch(err=>{
                    self.error = err.response.data;
                })
            },
            close() {
                this.$emit('close');
            },
            ...mapActions(['notify_error'])
        }
    }
</script>

<style scoped>

</style>
