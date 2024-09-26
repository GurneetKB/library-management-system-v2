<template>
    <div class="modal" :id="'viewSectionModal' + sectionId" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ newSection.title }}</h5>
                </div>
                <div class="modal-body">
                    <form class="form-floating">
                        <input type="email" class="form-control" id="floatingInputValue" placeholder="name@example.com"
                            v-model="newSection.title" required />
                        <label for="floatingInputValue">Section Title</label>
                    </form>
                    <div class="form-floating">
                        <input type="date" class="form-control" id="floatingInputValue" placeholder=""
                            v-model="newSection.date" required />
                        <label for="floatingInputValue">Date</label>
                    </div>
                    <div class="form-floating">
                        <textarea class="form-control" placeholder="Add a description here" id="floatingTextarea"
                            v-model="newSection.description" required></textarea>
                        <label for="floatingTextarea">Description</label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" @click="updateSection">Update</button>
                    <button type="button" class="btn btn-danger" @click="deleteSection">Delete</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
export default {
    name: 'ViewSectionModal',
    props: {
        sectionId: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            newSection: {
                id: '',
                title: '',
                date: '',
                description: ''
            }
        }
    },
    methods: {
        async updateSection() {
            try {
                const response = await axios.put(
                    `http://127.0.0.1:5000/api/genres/new/${this.sectionId}`,
                    {
                        section_name: this.newSection.title,
                        section_created_date: this.newSection.date,
                        section_descp: this.newSection.description,
                    },
                    {
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                        },
                    }
                );

                if (response.status === 200) {
                    console.log(response.data.msg);
                    location.reload();
                } else {
                    console.log(response.data.msg);
                    location.reload();
                }
            } catch (error) {
                console.error("Error fetching sections:", error);
            }
        },
        async deleteSection() {
            try {
            const response = await axios.delete(
                `http://127.0.0.1:5000/api/genres/new/${this.sectionId}`,
                {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
                }
            );

            if (response.status === 200) {
                console.log(response.data.msg);
                location.reload();
            } else {
                console.log(response.data.msg);
                location.reload();
            }
            } catch (error) {
            console.error("Error fetching sections:", error);
            }
        },
        fetchSections() {
            axios.get("http://127.0.0.1:5000/api/genres/new/"+this.sectionId, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
                },
            })
            .then((response) => {
                this.newSection.id = response.data.section_id;
                this.newSection.title = response.data.section_name;
                this.newSection.date = response.data.section_creation_date;
                this.newSection.description = response.data.section_descp;
                console.log(this.newSection);
            })
            .catch((error) => {
                console.error("Error fetching sections:", error);
            });
        },
    },
    mounted() {
        this.fetchSections();
    }
}
</script>

<style scoped></style>