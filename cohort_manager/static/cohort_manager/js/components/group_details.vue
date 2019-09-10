<template>
  <b-container class="aat-details-container aat-form-section" fluid>
    <b-row>
      <b-col class="aat-group-info-primary">
        <b-row>Cohort <span class="aat-group-data">25</span></b-row>
        <b-row>Applications Assigned <span class="aat-group-data">412</span></b-row>
      </b-col>
      <b-col class="aat-group-info-secondary">
        <b-row>Residency <span class="aat-group-data">wa-res</span></b-row>
        <b-row>Admit Decision<span class="aat-group-data">Admit</span></b-row>
        <b-row>Protected Group <span class="aat-group-data">No</span></b-row>
      </b-col>
      <b-col class="aat-group-info-secondary">
        <b-row>Decision<span class="aat-group-data">WA Resident general admits</span></b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
  export default {
    name: "GroupDetails",
    components: {},
    data(){
      return {
        
      };
    },
    mounted() {

    },
    methods: {

      },
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  @import '../../css/custom.scss';

  .aat-form-section {
    &.aat-details-container {
      border: solid #777 1px;
      margin: 3rem 0;
      max-width: 800px;
      padding: 2rem;
    }
  }

  .aat-group-info-primary .row {
    justify-content: center;
  }

  .aat-group-data {
    font-weight: bold;
  }

</style>
