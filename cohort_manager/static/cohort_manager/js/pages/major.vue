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
        current_period: undefined,
        loading_collection: true,
        periods: []
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
        properties['currentPeriod'] = this.current_period;
        properties['loadingCollection'] = this.loading_collection;
        properties['periods'] = this.periods;
        return properties;
      }
    },
    created (){
      this.current_period = this.$attrs.cur_period;
      this.periods = this.$attrs.periods;
      this.get_majors_for_period();
      EventBus.$on('period_change', period => {
        this.current_period = period;
        this.get_majors_for_period();
      });
    },
    mounted() {
      this.get_majors_for_period();
    },
    methods: {
      get_majors_for_period(){
        this.loading_collection = true;
        axios.get(
          '/api/collection/major/' + this.current_period + "/"
        ).then(response => {
          this.loading_collection = false;
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

