<template>
  <div v-if="messageString" id="alert_container" role="alert" class="aat-alert">
    <p>Successfully created {{ messageString }}</p>
  </div>
</template>

<script>
  export default {
    name: "MessageArea",
    components: {
    },
    props: {
      messageString: {
        type: String,
        default: ""
      },
    },
    data() {
      return {
        id: ''
      };
    },
    methods: {
    }
  };
</script>

<style lang="scss">

</style>
