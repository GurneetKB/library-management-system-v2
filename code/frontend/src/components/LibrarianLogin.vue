<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-primary text-white">
            <h3 class="mb-0">Librarian Login</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="loginLibrarian">
              <div class="mb-3">
                <label for="email" class="form-label">Email:</label>
                <input type="email" id="email" class="form-control" v-model="email" required>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password:</label>
                <input type="password" id="password" class="form-control" v-model="password" required>
              </div>
              <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async loginLibrarian() {
      try {
        const response = await fetch('http://localhost:5000/api/librarianlogin', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });
        const data = await response.json();
        if (data.accessToken) {
          localStorage.setItem('accessToken', data.accessToken);
          localStorage.setItem('user', JSON.stringify(data.userName));
          this.$router.push('/librarian/dashboard');
          console.log(data);
        }
      } catch (error) {
        console.error('Error logging in as librarian:', error);
      }
    }
  }
};
</script>
