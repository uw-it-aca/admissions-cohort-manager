<template>
  <div>
    <p>this is the import uploader component</p>
    <form @submit.prevent="handleUpload">
      Cohort:
      <select v-model="cohort_id" name="cohort">
        <option value="1">
          1
        </option>
        <option value="2">
          2
        </option>
        <option value="3">
          3
        </option>
      </select>
      <br>
      <input id="file" ref="file" type="file">
      <br>
      Comment: <textarea v-model="comment" />
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
        cohort_id: '',
        comment: '',
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
        formData.append('cohort_id', this.cohort_id);
        formData.append('comment', this.comment);

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
