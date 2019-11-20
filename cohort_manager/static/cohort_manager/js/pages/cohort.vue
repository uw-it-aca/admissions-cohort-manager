<template>
  <div>
    <h1 id="aat_page_header" class="aat-page-header">
      Assign to Cohort
    </h1>
    <upload v-bind="currentProperties" v-on="$listeners" />
  </div>
</template>

<script>
  import Upload from "../components/collection_upload.vue";
  const axios = require("axios");

  export default {
    name: "Cohort",
    components: {
      upload: Upload,
    },
    data(){
      return {
        has_uploaded: false,
        upload_response: undefined,
        cohort_options: [
        ]
      };
    },
    computed: {
      currentComponent: function () {
        if(this.has_uploaded){
          return "uploadReview";
        } else {
          return "upload";
        }

      },
      currentProperties: function() {
        var properties = {collectionType: 'Cohort'};
        if(this.has_uploaded){
          properties['uploadResponse'] = this.upload_response;
        }
        properties['collectionOptions'] = this.cohort_options;
        properties['uploadResponse'] = this.upload_response;
        return properties;
      }
    },
    mounted() {
      axios.get(
        '/api/collection/cohort/'
      ).then(response => {
        this.cohort_options = response.data;
      });
    },
    methods: {
      onFileUpload(response){
        this.has_uploaded = true;
        this.upload_response = response.data;
      }
    }
  };
</script>

<style lang="scss">
</style>
