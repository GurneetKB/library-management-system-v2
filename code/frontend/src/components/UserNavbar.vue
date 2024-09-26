<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <router-link to="/user/dashboard" class="nav-link" activeClassName="active">User Dashboard</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/user/dashboard/my-books" class="nav-link" activeClassName="active">My Books</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/dashboard/all-books" class="nav-link" activeClassName="active">All Books</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/dashboard/all-stats" class="nav-link" activeClassName="active">Stats</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/dashboard/my-request" class="nav-link" activeClassName="active">Requests</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/profile" class="nav-link" activeClassName="active">Profile</router-link>
            </li>
          </ul>
          <button class="btn btn-outline-danger" style="margin-left: 10px" @click="logout">Logout</button>
        </div>
      </div>
    </nav>
  </div>
</template>

<style>
</style>

<script>
export default {
  name: "UserNavbar",
  methods:{
    logout(){
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user');
        this.$router.push('/');
    }
  }
};
</script>