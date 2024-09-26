<template>
  <div class="admin-dashboard">
    <LibrarianNavbar />
    <div class="container mt-4">
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h4>Top Books</h4>
            </div>
            <div class="card-body">
              <Chart type="bar" :data="chartData" class="h-[30rem]" />
            </div>

          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h4>Most Requested Books</h4>
            </div>
            <div class="card-body">
              <Chart type="bar" :data="bookChartData" class="h-[30rem]" />
            </div>

          </div>
        </div>
      </div>
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h4>Users Activity</h4>
            </div>
            <div class="card-body">
              <Chart type="bar" :data="userActivityData" class="h-[30rem]" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LibrarianNavbar from "@/components/LibrarianNavbar.vue";
import axios from "axios";
import Chart from 'primevue/chart';


export default {
  name: "StatsSection",
  components: {
    LibrarianNavbar,
    Chart
  },
  data() {
    return {
      chartData: null,
      bookChartData: null,
      userActivityData: null
    };
  },
  mounted() {
    this.getTopReader(),
    this.getTopRequestedBooks(),
    this.getUserActivity()
  },
  methods: {
    async getTopReader() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/top/readers", 
          { headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` } }
        );
        console.log(response.data);
        this.chartData = response.data;
      } catch (error) {
        console.error("Error fetching book count:", error);
      }
    },
    async getTopRequestedBooks() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/top/books/requested", 
          { headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` } }
        );
        console.log(response.data);
        this.bookChartData = response.data;
      } catch (error) {
        console.error("Error fetching book count:", error);
      }
    },
    async getUserActivity() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/user/activity", 
          { headers: { Authorization: `Bearer ${localStorage.getItem("accessToken")}` } }
        );
        console.log(response.data);
        this.userActivityData = response.data;
      } catch (error) {
        console.error("Error fetching book count:", error);
      }
    }
  },
};
</script>

<style scoped>
.statistics {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 3rem;
}
</style>