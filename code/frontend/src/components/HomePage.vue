<template>
  <div class="container text-center mt-5">
    <h1>Welcome to the Bookstore</h1>
    <p class="lead">
      Welcome to the home page of our bookstore. Please click the button below to
      login
    </p>
    <div class="btn-group mt-5" role="group" aria-label="Basic outlined example">
      <router-link to="/api/userlogin" class="btn btn-outline-primary me-2">
        User Login
      </router-link>
      <router-link to="/api/usersignup" class="btn btn-outline-primary me-2">
        User Signup
      </router-link>
      <router-link to="/api/librarianlogin" class="btn btn-outline-primary me-2">
        Librarian Login
      </router-link>
    </div>
  </div>
</template>

<script>

export default {
  name: "HomePage",
  components: {
  },
};
</script>

<style scoped>
</style>
