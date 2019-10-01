<template>
  <b-container fluid>
    <b-row>
      <b-col>
        <b-pagination
          class="aat-activity-pagination"
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          size="sm"
          aria-controls="assignment_history_table"
        />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12" lg="9" order-lg="1" order="2" class="aat-col-nopad aat-activity-table">
        <b-table 
          id="assignment_history_table"
          responsive
          striped
          show-empty
          small
          class="aat-data-table"
          :items="activities"
          :fields="activityFields"
          :current-page="currentPage"
          :per-page="perPage"
          :filter="filter"
        >
          <template v-slot:cell(selection)="row">
            <a href="www.tableau.com" :title="'View filters in Tableau'"><i class="fas fa-filter" /><span class="sr-only">Filters</span></a>
          </template>
        </b-table>
      </b-col>

      <b-col order-lg="2" order="1">
        <b-form class="aat-filter-form" @reset="onReset">
          <h2 class="aat-filter-title">
            Filter
          </h2>
          <span class="aat-filter-reset">
            <b-button type="reset" variant="link" @click="getAllActivities">
              Reset
            </b-button>
          </span>
          <b-form-group
            label="Assignment Type"
            label-size="sm"
            label-for="as_type_filter"
          >
            <b-input-group size="sm">
              <b-form-select
                id="as_type_filter"
                v-model="astypeFilter"
                class="aat-filter-select"
                :options="astypeOptions"
                @change="getAssignmentActivities"
              >
                <template v-slot:first>
                  <option :value="null" disabled>
                    -- Select --
                  </option>
                </template>
              </b-form-select>
            </b-input-group>
          </b-form-group>

          <b-form-group
            label="Cohort"
            label-size="sm"
            label-for="cohort_filter"
          >
            <b-input-group size="sm">
              <b-form-select
                id="cohort_filter"
                v-model="cohortFilter"
                class="aat-filter-select"
                :options="cohortOptions"
                @change="getCohortActivities"
              >
                <template v-slot:first>
                  <option :value="null" disabled>
                    -- Select --
                  </option>
                </template>
              </b-form-select>
            </b-input-group>
          </b-form-group>

          <b-form-group
            label="Major"
            label-size="sm"
            label-for="major_filter"
          >
            <b-input-group size="sm">
              <b-form-select
                id="major_filter"
                v-model="majorFilter"
                class="aat-filter-select"
                :options="majorOptions"
                @change="getMajorActivities"
              >
                <template v-slot:first>
                  <option :value="null" disabled>
                    -- Select --
                  </option>
                </template>
              </b-form-select>
            </b-input-group>
          </b-form-group>

          <b-form-group
            label="System Key"
            label-size="sm"
            label-for="SysKeyInput"
          >
            <b-input-group size="sm">
              <b-form-input
                id="SysKeyInput"
                v-model="syskeyFilter"
                placeholder="Type to Search"
                @change="getSyskeyActivities"
              />
            </b-input-group>
          </b-form-group>
        </b-form>
      </b-col>
    </b-row>
  </b-container>
</template>



<script>
  const axios = require("axios");
  export default {
    name: "ActivityList",
    components: {
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },
    },
    data(){
      return {
        activityFields: [
          {
            key: 'activity_date',
            label: "Date/Time",
            class: "aat-data-cell aat-data-nowrap",
            sortable: true
          },
          {
            key: 'assigned_msg',
            label: 'Assignment',
            class: "aat-data-cell",
            sortable: false
          },
          {
            key: 'submitted_msg',
            label: 'Submitted',
            class: "aat-data-cell",
            sortable: false
          },
          {
            key: 'selection',
            class: "aat-data-cell",
            sortable: false,
          },
          {
            key: 'comment',
            class: "aat-data-cell",
            sortable: false,
          },
          {
            key: 'user',
            class: "aat-data-cell",
            sortable: false
          },
        ],
        activities: [],
        astypeFilter: null,
        astypeOptions: [
          { value: 'cohort', text: 'Cohort' },
          { value: 'major', text: 'Major' }
        ],
        cohortFilter: null,
        cohortOptions: [
          { value: '1', text: '1' },
          { value: '2', text: '2' },
          { value: '3', text: '3' },
          { value: '99', text: '99' }
        ],
        majorFilter: null,
        majorOptions: [
          { value: 'astr', text: 'ASTR' },
          { value: 'biol', text: 'BIOL' },
          { value: 'cse', text: 'CSE' },
          { value: 'hcde', text: 'HCDE' }
        ],
        syskeyFilter: null,
        totalRows: 1,
        currentPage: 1,
        perPage: 20,
        filter: null,
        filterOn: [],
      };
    },
    mounted() {
      // Set the initial number of items
      this.totalRows = this.activities.length;
      this.getAllActivities();
    },
    methods: {
      onFiltered(filteredItems) {
        // Trigger pagination to update the number of buttons/pages due to filtering
        this.totalRows = filteredItems.length;
        this.currentPage = 1;
      },
      onReset(evt) {
        evt.preventDefault();
        // Reset our form values
        this.astypeFilter = null;
        this.cohortFilter = null;
        this.majorFilter = null;
        this.syskeyFilter = '';
        // Trick to reset/clear native browser form validation state
        this.show = false;
        this.$nextTick(() => {
          this.show = true;
        });
      },
      getMajorActivities(major_id){
        this.getActivities("?major_id=" + major_id);
      },
      getCohortActivities(cohort_id){
        this.getActivities("?cohort_id=" + cohort_id);
      },
      getAssignmentActivities(assignment_type){
        this.getActivities("?assignment_type=" + assignment_type);
      },
      getSyskeyActivities(syskey){
        this.getActivities("?system_key=" + syskey);
      },
      getAllActivities() {
        this.getActivities("");
      },
      getActivities(filter_string){
        axios.get(
          '/api/activity/' + filter_string,
        ).then(response => {
          if(response.status === 200){
            this.activities = response.data.activities;
          }
        });
      }
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  @import '../../css/custom.scss';

  .aat-col-nopad {
    padding: 0;
  }

  .aat-activity-pagination {
    float: right;
  }

  .aat-filter-form {
    border-top: 1px solid #dee2e6;
    padding: 0.75rem 1.5rem;
  }
  
  .aat-filter-select {
    background: none;
  }

  .aat-filter-title {
    float: left;
    font-size: 1rem;
    font-weight: bold;
    line-height: inherit;
  }

  .aat-filter-reset button {
    float: right;
    padding: 0;
  }

</style>
