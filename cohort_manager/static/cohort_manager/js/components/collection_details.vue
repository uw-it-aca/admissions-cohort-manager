<template>
  <b-container class="aat-details-container aat-form-section" fluid>
    <b-row>
      <b-col cols="12" md="3" class="aat-group-info-primary">
        <b-row class="aat-info-spacing"><div class="aat-data-primary">Cohort</div> <div class="aat-group-data aat-data-primary">25</div></b-row>
        <b-row><div class="aat-data-primary">Applications Assigned</div> <div class="aat-group-data aat-data-primary">412</div></b-row>
      </b-col>
      <b-col cols="12" md="4" class="aat-group-info-secondary">
        <b-row class="aat-info-spacing">Residency <span class="aat-group-data">wa-res</span></b-row>
        <b-row class="aat-info-spacing">Admit Decision<span class="aat-group-data">Admit</span></b-row>
        <b-row>Protected Group <span class="aat-group-data">No</span></b-row>
      </b-col>
      <b-col cols="12" md="5" class="aat-group-info-secondary">
        <b-row>Decision<span class="aat-group-data">WA Resident general admits</span></b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
  export default {
    name: "CollectionDetails",
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
      font-size: 0.85rem;
      line-height: 1.5;
      margin: 1.5rem 0 0;
      max-width: 800px;
      padding: 2rem;
    }

    .row {
      margin: 0;
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
      font-weight: normal;
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

  .aat-data-primary {
    margin: auto;
    text-align: center;
  }

  .aat-info-spacing {
    padding-bottom: 1.5rem;
  }

  @media screen and (max-width: 767px) {
    .aat-group-info-primary {
      margin-bottom: 2rem;
      text-align: center;
    }

    .aat-group-info-secondary {
      margin-bottom: 1rem;
      text-align: center;
    }

  }

</style>
