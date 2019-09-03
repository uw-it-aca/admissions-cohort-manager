<template>
  <div>
    <p>this is the import uploader component</p>
    <form @submit.prevent="handleUpload">
      <input id="file" ref="file" type="file">
      <input type="submit" value="Upload">
    </form>
  </div>
</template>

<script>
  const axios = require("axios");
  import Vue from "vue/dist/vue.esm.js";
  import VueCookies from "vue-cookies";
  Vue.use(VueCookies);
  export default {
    name: "Upload",
    components: {},
    data(){
      return {
        file: '',
        csrfToken: '',
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
          this.$emit('uploaded', response);
        }). catch(function(){
          // this.uploadResponse = "THERE WAS AN ERROR";
        });
      }
    }
  };
</script>

<style lang="scss">
</style>
