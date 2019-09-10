<template>
  <div>
    <form @submit.prevent="handleUpload">
      <fieldset class="aat-form-section">
        <legend class="aat-sub-header">
          Select {{ collectionType }}
        </legend>
        <label for="collection_chooser">Assign applications to {{ collectionType }} </label>
        <b-form-select id="collection_chooser" v-model="collection_id" name="collection" :options="collection_options" class="aat-select-inline" />
      </fieldset>
      <groupdetails />
      <fieldset class="aat-form-section">
        <legend class="aat-sub-header">
          Enter Applications
        </legend>
        <input id="file" ref="file" type="file" class="aat-file-input"> <div>or <a href="#">manually by system keys</a></div>
        <div id="file_name" />
      </fieldset>
      <fieldset class="aat-form-section">
        <legend class="aat-sub-header">
          Add Comment
        </legend>
        <label for="assginment_comment">Enter comment for this assignment</label>
        <textarea id="assignment_comment" v-model="comment" class="aat-comment-field" />
      </fieldset>
      <input type="submit" value="Upload">
    </form>
  </div>
</template>

<script>
  const axios = require("axios");
  import GroupDetails from "../components/group_details.vue";
  import Vue from "vue/dist/vue.esm.js";
  import VueCookies from "vue-cookies";
  Vue.use(VueCookies);
  export default {
    name: "Upload",
    components: {
      groupdetails: GroupDetails
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },
    },
    data(){
      return {
        file: '',
        collection_id: null,
        collection_options: [
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
        formData.append('comment', this.comment);
        if (this.collectionType == "Cohort") {
          formData.append('cohort_id', this.collection_id);
        } else if (this.collectionType == "Major") {
          formData.append('major_id', this.collection_id);
        } else {
          this.uploadResponse = "THERE WAS AN ERROR";
          return;
        }

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
          this.uploadResponse = "THERE WAS AN ERROR";
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
    padding: 0;
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
    padding: 0.5rem;
    width: 100%;
  }

</style>