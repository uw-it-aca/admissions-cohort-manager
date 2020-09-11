<template>
  <div class="aat-env-test">
    This is AAT Test.
  </div>
</template>

<script>
  export default {
    name: "EnvBanner",
    components: {
    },
    data() {
      return {

      };
    },
    computed: {
    },
    mounted() {
    },
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';

  .aat-env-test {
    background-color: $test-env-bkgnd;
    border-bottom: solid 2px $test-env-border;
    color: #fff;
    font-size: 0.9rem;
    font-weight: bold;
    padding: 0.5rem 1rem;
    text-align: center;
  }
</style>
