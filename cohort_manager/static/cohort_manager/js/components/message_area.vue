<template>
  <div v-if="messageString" id="alert_container" role="alert" class="aat-alert">
    <b-alert variant="success" show>
      {{ messageString }}
    </b-alert>
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
  .aat-alert {
    margin: 1rem auto;
    max-width: 100%;
  }
</style>
