<template>
  <div>
    <p>this is the import page stub</p>
    <upload @uploaded="onFileUpload" />
    <div>
      {{ upload_response }}
    </div>
  </div>
</template>

<script>
  import Upload from "../components/upload.vue";

  export default {
    name: "Import",
    components: {
      upload: Upload
    },
    data(){
      return {
        upload_response: undefined,
      };
    },
    mounted() {
    },
    methods: {
      onFileUpload(response){
        this.upload_response = response;
      }
    }
  };
</script>

<style lang="scss">
</style>
