const AddBook = {
    template:`
    <div class="creationform2">
    <div class="container">
        <h3 align="center">Add New Book</h3> <br>
        <form method="POST" action="/add-book-2">
            <div class="mb-3">
                <label for="BookName" class="form-label">Book Name</label>
                <input type="text" class="form-control" id="BookName" name="bookName">
            </div>
            <div class="mb-3">
                <label for="AuthorName" class="form-label">Author Name</label>
                <input type="text" class="form-control" id="AuthorName" name="authorName"></input>
            </div>
            <input type="hidden" name="sectionName" :value="$route.query.SectionName">
            <div class="mb-3">
                <h5>Book Section : {{ $route.query.SectionName }}</h5>
            </div><br>
            <div class="row" align="center">
                <div class="col">
                    <button type="submit" class="btn btn-primary">Submit</button>
                </div>
                <div class="col">
                    <router-link to="/" class="btn btn-danger">Close</router-link>
                </div>
            </div>
      </form>
    </div>
</div>
    `
};



const EditBook = {
    template:`
    <div class="creationform2">
    <div class="container">
        <h3 align="center">Edit Book Details</h3> <br>
        <form method="POST" action="/edit-book">
            <div class="mb-3">
                <input type="hidden" id="SectionID" name="SectionID" :value="$route.query.SecID">
                <input type="hidden" id="BookID" name="BookID" :value="$route.query.BookID">
                <label for="BookName" class="form-label">Book Name</label>
                <input type="text" class="form-control" id="BookName" name="BookName" :value="$route.query.BookName">
            </div>
            <div class="mb-3">
                <label for="AuthorName" class="form-label">Author Name</label>
                <input type="text" class="form-control" id="AuthorName" name="AuthorName" :value="$route.query.Author"></input>
            </div>
            <div class="row" align="center">
                <div class="col">
                    <button type="submit" class="btn btn-primary">Submit</button>
                </div>
                <div class="col">
                    <router-link to="/" class="btn btn-danger">Close</router-link>
                </div>
            </div>
      </form>
    </div>
</div>
    `
};


const routes = [
    { path: '/add-book-2', component: AddBook },
    { path: '/edit-book', component: EditBook }
];

const router = new VueRouter({
    routes
});

const app = new Vue({
    el: '#app',
    router
});
