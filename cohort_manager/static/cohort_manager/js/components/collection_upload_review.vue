<template>
  <div>
    <div id="file_name">
      {{ uploaded_filename }}
    </div>
    <p id="upload_app_count" class="aat-status-feedback">
      {{ upload_count }} system keys found.
    </p>
  </div>
</template>

<script>
  import Vue from "vue/dist/vue.esm.js";
  import VueCookies from "vue-cookies";
  Vue.use(VueCookies);
  export default {
    name: "UploadReview",
    components: {},
    props: {
      uploadResponse: {
        type: Object,
        default: function() {return {};}
      },
      collectionType: {
        type: String,
        default: ""
      }
    },
    data(){
      return {
        upload_count: 0,
        collection_id: '',
        uploaded_filename: ''
      };
    },
    mounted() {
      this.upload_count = this.$props.uploadResponse.assignments.length;
      if(this.$props.collectionType === "Cohort"){
        this.collection_id = this.$props.uploadResponse.assignments[0].cohort;
      }
      else if(this.$props.collectionType === "Major"){
        this.collection_id = this.$props.uploadResponse.assignments[0].major;
      }
      this.uploaded_filename = this.$props.uploadResponse.upload_filename;
    },
    methods: {
    }
  };
</script>

<style lang="scss">
</style>
