<template>
  <b-container class="aat-details-container aat-form-section" fluid>
    <b-row>
      <b-col cols="12" md="4" class="aat-group-info-primary">
        <b-row class="aat-info-spacing"><div>Cohort</div> <div class="aat-group-data">25</div></b-row>
        <b-row>Applications Assigned <span class="aat-group-data">412</span></b-row>
      </b-col>
      <b-col cols="12" md="4" class="aat-group-info-secondary">
        <b-row class="aat-info-spacing">Residency <span class="aat-group-data">wa-res</span></b-row>
        <b-row class="aat-info-spacing">Admit Decision<span class="aat-group-data">Admit</span></b-row>
        <b-row>Protected Group <span class="aat-group-data">No</span></b-row>
      </b-col>
      <b-col cols="12" md="4" class="aat-group-info-secondary">
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
      color: #777;
      font-size: 1rem;
      line-height: 1;
      margin: 1.5rem 0 0;
      max-width: 800px;
      padding: 2rem;
    }

    .row {
      align-items: center;
      justify-content: center;
    }
  }

  .aat-group-info-primary {
    .row {
      flex-direction: column-reverse;
    }

    .aat-group-data {
      font-size: 2rem;
      
    }
  }

  .aat-group-info-secondary {
    .row {
      align-items: unset;
      flex-direction: column;
      font-size: 0.85rem;
      font-weight: normal;
      line-height: 1.5;
      margin: 0 auto;
      padding: 0 25%;
    }

    .aat-group-data {
      font-size: 1rem;
      font-weight: normal;
    }

    .aat-info-spacing {
      padding-bottom: 1rem;
    }
  }

  .aat-group-data {
    color: $text-color;
    font-weight: bold;
  }

  .aat-info-spacing {
    padding-bottom: 2.5rem;
  }

</style>
