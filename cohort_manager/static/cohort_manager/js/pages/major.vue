<template>
  <div>
    <h1 class="aat-page-header">
      Assign Major
    </h1>
    <upload collection-type="Major" @uploaded="onFileUpload" />
    <div>
      {{ upload_response }}
    </div>
  </div>
</template>

<script>
  import Upload from "../components/collection_upload.vue";
  export default {
    name: "Major",
    components: {
      upload: Upload
    },
    data(){
      return {
        upload_response: undefined,
      };
    },
    mounted() {},
    methods: {
      onFileUpload(response){
        this.upload_response = response;
      }
    }
  };
</script>

<style lang="scss">
</style>
