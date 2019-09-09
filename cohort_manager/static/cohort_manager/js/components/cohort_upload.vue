<template>
  <div>
    <form @submit.prevent="handleUpload" >
      <fieldset class="aat-form-section">
        <legend class="aat-sub-header">Select Cohort</legend> 
        <label for="cohort_chooser">Assign applications to Cohort </label>
        <b-form-select id="cohort_chooser" v-model="cohort_id" name="cohort" :options="cohort_options" class="aat-select-inline">
        </b-form-select>
      </fieldset>
      <fieldset class="aat-form-section">
        <legend class="aat-sub-header">Enter Applications</legend> 
        <input id="file" ref="file" type="file" class="aat-file-input"> <div>or <a href="#">manually by system keys</a></div>
        <div id="file_name"></div>
      </fieldset>
      <fieldset class="aat-form-section">
        <legend class="aat-sub-header">Add Comment</legend> 
        <label for="assginment_comment">Enter comment for this assignment</label> 
        <textarea id="assignment_comment" v-model="comment" class="aat-comment-field" />
      </fieldset>
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
        cohort_id: null,
        cohort_options: [
          {value: '1', text: '1'},
          {value: '2', text: '2'},
          {value: '99', text: '99'},
        ],
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
  @import '../../css/_variables.scss';
  @import '../../css/custom.scss';

  .aat-select-inline {
    background: none;
    border-color: $text-color;
    border-radius: 0;
    border-style: none none solid;
    margin: -0.25rem 0.5rem 0;
    width: 3rem;
  }

  .aat-file-input {
    padding: 1rem 0;
  }

  .aat-comment-field {
    display: block;
    height: 144px;
    max-width: 650px;
    min-width: 250px;
    padding: 8px;
    width: 100%;
  }

</style>
