<template>
  <div>
    <UserNavbar />
    <div class="container mt-4">
      <div class="row">
        <div class="col-md-4">
          <div class="card">
            <div class="card-body text-center">
              <h4>Total Books</h4>
              <h3>{{ book_count }}</h3>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-body text-center">
              <h4>Completed Books</h4>
              <h3>{{ allocated_book_count }}</h3>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card">
            <div class="card-body text-center">
              <h4>Requested Books</h4>
              <h3>{{ reqested_count }}</h3>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h4>Recommended Books</h4>
            </div>
            <div class="card-body">
              <table class="table">
                <thead>
                  <tr>
                    <th scope="col">name</th>
                    <th scope="col">author</th>
                    <th scope="col">section name</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="book in top_books" :key="book.id">
                    <td>{{ book.name }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.section_name }}</td>
                  </tr>
                </tbody>
              </table>
              <router-link to="/user/dashboard/all-books" class="btn btn-primary">View</router-link>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h4>Books To Return</h4>
            </div>
            <div class="card-body">
              <table class="table">
                <thead>
                  <tr>
                    <th scope="col">name</th>
                    <th scope="col">author</th>
                    <th scope="col">section name</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="book in book_by_req" :key="book.id">
                    <td>{{ book.name }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.section_name }}</td>
                  </tr>
                </tbody>
              </table>
              <router-link to="/user/dashboard/my-books" class="btn btn-primary">View</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import axios from "axios";
export default {
  data() {
    return {
      section_count: 0,
      reqested_count: 0,
      allocated_book_count: 0,
      book_count: 0,
      top_books: [],
      book_by_req: [],
      inactive_users: [],
      active_users: []
    };
  },
  name: "UserDashboard",
  components: {
    UserNavbar,
  },
  methods: {
    async setUsersLastVisitTime() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/api/track-last-login", {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          }
        });
        const data = await response.data;
        if (response.status === 200) {
          console.log("Last login time updated: ", data);
        } else {
          console.error("Failed to update last login time: ", data.error);
        }
      } catch (error) {
        console.error("Error updating last login time: ", error);
      }
    },
    async getDashboardData() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/dashboard", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          }
        });
        const data = await response.data;
        if (response.status === 200) {
          console.log("Dashboard data: ", data);
          this.section_count = data.section_count;
          this.reqested_count = data.reqested_count;
          this.allocated_book_count = data.allocated_book_count;
          this.book_count = data.book_count;
          this.top_books = data.top_books;
          this.book_by_req = data.book_by_req;
          this.inactive_users = data.inactive_users;
          this.active_users = data.active_users;
        } else {
          console.error("Failed to fetch dashboard data: ", data.error);
        }
      } catch (error) {
        console.error("Error fetching dashboard data: ", error);
      }
    },
  },
  mounted() {
    this.userName = JSON.parse(localStorage.getItem("user"));
    this.setUsersLastVisitTime();
    this.getDashboardData();
  },
};
</script>


<style scoped>
.user-info {
  text-align: center;
  margin-top: 20px;
}
</style>