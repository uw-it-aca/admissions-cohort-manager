<template>
  <div>
    <h1 id="aat_page_header" class="aat-page-header">
      Assign to Major
    </h1>
    <upload v-bind="currentProperties" v-on="$listeners" />
  </div>
</template>

<script>
  import Upload from "../components/collection_upload.vue";
  import { EventBus } from "../main";
  const axios = require("axios");

  export default {
    name: "Major",
    components: {
      upload: Upload,
    },
    data(){
      return {
        has_uploaded: false,
        upload_response: undefined,
        major_options: [],
        current_period: undefined
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
        var properties = {collectionType: 'Major'};
        if(this.has_uploaded){
          properties['uploadResponse'] = this.upload_response;
        }
        properties['collectionOptions'] = this.major_options;
        return properties;
      }
    },
    created (){
      EventBus.$on('period_change', period => {
        this.current_period = period;
        this.get_majors_for_period();
      });
    },
    mounted() {
    },
    methods: {
      get_majors_for_period(){
        axios.get(
          '/api/collection/major/' + this.current_period + "/"
        ).then(response => {
          this.major_options = response.data;
        });
      },
      onFileUpload(response){
        this.has_uploaded = true;
        this.upload_response = response.data;
      }
    }
  };
</script>

<style lang="scss">
</style>

