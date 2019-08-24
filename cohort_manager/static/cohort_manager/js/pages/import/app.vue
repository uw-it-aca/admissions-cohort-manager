<template>
  <div>
    <p>this is the import page stub</p>
    <form @submit.prevent="handleUpload">
      <input id="file" ref="file" type="file">
      <input type="submit" value="Upload">
    </form>
    <div>
      {{ uploadResponse }}
    </div>
  </div>
</template>

<script>
  const axios = require("axios");
  import Vue from "vue/dist/vue.esm.js";
  import VueCookies from "vue-cookies";
  Vue.use(VueCookies);
  export default {
    name: "Import",
    components: {},
    data(){
      return {
        file: '',
        csrfToken: '',
        uploadResponse: ''
      };
    },
    mounted() {
      this.setCSRF();
    },
    methods: {
      setCSRF(){
        this.csrfToken = $cookies.get("csrftoken");
      },

      handleUpload() {
        this.file = this.$refs.file.files[0];
        let formData = new FormData();
        formData.append('file', this.file);

        axios.post(
          '/api/upload',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              'X-CSRFToken': this.csrfToken
            }
          }
        ).then(response => {
          this.uploadResponse = response.data;
        }). catch(function(){
          this.uploadResponse = "THERE WAS AN ERROR";
        });
      }
    }
  };
</script>

<style lang="scss">
</style>
