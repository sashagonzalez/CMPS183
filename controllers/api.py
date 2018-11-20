# Here go your api methods.


@auth.requires_signature()
def add_post():
    post_id = db.post.insert(
        post_title=request.vars.post_title,
        post_description=request.vars.post_description,
    )
    # We return the id of the new post, so we can insert it along all the others.
    return response.json(dict(post_id=post_id))


def get_post_list():
    results = []
    if auth.user is None:
        # Not logged in.
        rows = db().select(db.post.ALL, orderby=~db.post.post_time)
        for row in rows:
            results.append(dict(
                id=row.id,
                post_title=row.post_title,
                post_content=row.post_content,
                post_author=row.post_author,
                thumb = None,
            ))
    else:
        # Logged in.
        rows = db().select(db.post.ALL, db.thumb.ALL,
                            left=[
                                db.thumb.on((db.thumb.post_id == db.post.id) & (db.thumb.user_email == auth.user.email)),
                            ],
                            orderby=~db.post.post_time)
        for row in rows:
            results.append(dict(
                id=row.post.id,
                post_title=row.post.post_title,
                post_content=row.post.post_content,
                post_author=row.post.post_author,
                thumb = None if row.thumb.id is None else row.thumb.thumb_state,
                like = None if row.thumb.thumb_state is None else True if row.thumb.thumb_state is 'u' else False,
                dislike = None if row.thumb.thumb_state is None else True if row.thumb.thumb_state is 'd' else False,
            ))
    # For homogeneity, we always return a dictionary.
    return response.json(dict(post_list=results))


#def get_user_email():
#    u = auth.user.email
#    return(u)

def update_post():
    id = int(request.vars.post_id)
    title = request.vars.post_title
    content = request.vars.post_content
    db.post.update_or_insert(
            (db.post.id == id) & (db.post.post_author == auth.user.email),
            id = id,
            post_title = title,
            post_content = content
        )
    return "ok"

        

