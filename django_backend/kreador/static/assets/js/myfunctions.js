
function postAlbum() {
	const innerDiv = document.getElementById('image_upload').getElementsByClassName('dz-image')
	const innerinnerDiv = innerDiv.getElementsByClassName("dz-preview dz-processing dz-image-preview dz-success dz-complete")
	document.getElementById('upload_img2') = innerDiv.getElementsByClassName("dz-image").getElementsByTagName('img').src
	document.getElementById('postform').submit()
	}
	
	// function likeMedia(post_id, username) {
	// 	var url = username + '/post/' + post_id + '/like'
	
	// 	fetch(url, {
	// 		method: "POST",
	// 		headers: {
	// 		"Content-type": "application/json; charset=UTF-8"
	// 		}
	// 	}).then((response) => {
	// 		likecnt = parseInt(document.getElementById(post_id + '-likecnt').innerHTML)
	//     	likecnt = likecnt + 1
	//     	like_cnts = Array.from(document.getElementsByClassName(post_id + '-likecnt'))
	// 		like_cnts.forEach((like_cnt) => {like_cnt.innerHTML = likecnt})
	// 	})
	// }
	
	function likePost(user_name, post_id) {
	likeBtn = document.getElementById(post_id+'likebtn')
	if ( likeBtn.className === "bi bi-hand-thumbs-up-fill pe-1") {
		var url = '/'+user_name+'/post/' + post_id + '/unlike'
		document.getElementById(post_id + 'likebtn').className = "bi bi-hand-thumbs-up pe-1"
		likecnt = parseInt(document.getElementById(post_id + 'likecnt').innerHTML)
		likecnt = likecnt - 1
		document.getElementById(post_id + 'likecnt').innerHTML = likecnt
	} else if ( likeBtn.className === "bi bi-hand-thumbs-up pe-1" ) {
		var url = '/'+user_name+'/post/' + post_id + '/like'
		document.getElementById(post_id + 'likebtn').className = "bi bi-hand-thumbs-up-fill pe-1"
		likecnt = parseInt(document.getElementById(post_id + 'likecnt').innerHTML)
		likecnt = likecnt + 1
		document.getElementById(post_id + 'likecnt').innerHTML = likecnt
	} else if ( likeBtn.className === "bi bi-heart-fill pe-1" ) {
		var url = '/'+user_name+'/post/' + post_id + '/unlike'
		document.getElementById(post_id + 'likebtn').className = "bi bi-heart pe-1"
		likecnt = parseInt(document.getElementById(post_id + 'likecnt').innerHTML)
		likecnt = likecnt - 1
		document.getElementById(post_id + 'likecnt').innerHTML = likecnt
	} else if ( likeBtn.className === "bi bi-heart pe-1" ) {
		var url = '/'+user_name+'/post/' + post_id + '/like'
		document.getElementById(post_id + 'likebtn').className = "bi bi-heart-fill pe-1"
		likecnt = parseInt(document.getElementById(post_id + 'likecnt').innerHTML)
		likecnt = likecnt + 1
		document.getElementById(post_id + 'likecnt').innerHTML = likecnt
	}
	fetch(url, {
		method: "POST",
		headers: {
		"Content-type": "application/json; charset=UTF-8"
		}
	})
	}
	
	function likeCommentObj(cmtObjId, cmtObjType) {
		commentObjLikes = document.getElementById(cmtObjId + cmtObjType + "-likecount")
		commentObjLikes.style.pointerEvents="none"
	
		url = "/api/" + cmtObjType + "/like/"
		token = document.getElementById("replybox-template-form").children[0].value
		if (cmtObjType == 'comment') {
			data = {'comment': cmtObjId}
		} else if (cmtObjType == 'reply') {
			data = {'reply': cmtObjId}
		}
	
		if (commentObjLikes.classList == "nav-link bi bi-hand-thumbs-up") {
			// console.log("post")
			fetch(url, {
			method: "POST",
			headers: {
			"Content-type": "application/json; charset=UTF-8",
			'X-Requested-With': 'XMLHttpRequest',
			'X-CSRFToken': token
			},
			body: JSON.stringify(data)
			}).then(response => response.json()).then(response => {
			// console.log(response)
			commentObjLikes.className = "nav-link bi bi-hand-thumbs-up-fill"
			newLikeCount = parseInt(commentObjLikes.innerText[1]) + 1
			// console.log(newLikeCount)
			commentObjLikes.innerText = " " + String(newLikeCount)
			commentObjLikes.style.pointerEvents="auto"
			})
		} else if (commentObjLikes.classList == "nav-link bi bi-hand-thumbs-up-fill") {
			// console.log("delete")
			fetch(url, {
			method: "DELETE",
			headers: {
			"Content-type": "application/json; charset=UTF-8",
			'X-Requested-With': 'XMLHttpRequest',
			'X-CSRFToken': token
			},
			body: JSON.stringify(data)
			}).then(response => response.json()).then(response => {
			// console.log(response)
			commentObjLikes.className = "nav-link bi bi-hand-thumbs-up"
			newLikeCount = parseInt(commentObjLikes.innerText[1]) - 1
			// console.log(newLikeCount)
			commentObjLikes.innerText = " " + String(newLikeCount)
			commentObjLikes.style.pointerEvents="auto"
			})
		}
	
	}
	
	
	function removeFromContacts(usname, id) {
		url = '/' + usname + '/contacts/delete/' + id
		fetch(url, {method: "POST"}).then(response => response.json()).then( response => {
		//   console.log(response.text)
		  deletedContactCards = Array.from(document.getElementsByClassName(id+"-post"))
		//   console.log(deletedContactCards)
		  deletedContactCards.forEach(card => {
			card.remove()
		  })
		  if (document.getElementById(id+"-contactcard")) {
	// 		console.log("present sir")
			document.getElementById(id+"-contactcard").remove()
		  }
		  iziToast.success({
			title: response.text,
		});
		  contactCounts = Array.from(document.getElementsByClassName("contacts-count"))
		  contactCounts.forEach((contactCount) => {
			contactCount.innerHTML = parseInt(contactCount.innerHTML.trim()) - 1
		  })
		}
	
		)
		return false;
	  }
	
	function changeContacts(usname, id) {
		elem = document.getElementById(id + 'ctca')
		if (elem.className === "btn btn-primary-soft rounded-circle icon-md ms-auto") {
		  addToContacts(id, usname);
		  document.getElementById(id + 'ctca').className = "btn btn-primary rounded-circle icon-md ms-auto"
		  document.getElementById(id + 'ctci').className = "bi bi-person-check-fill";
		} else {
		  removeFromContacts(usname, id)
		  document.getElementById(id + 'ctca').className = "btn btn-primary-soft rounded-circle icon-md ms-auto"
		  document.getElementById(id + 'ctci').className = "fa-solid fa-plus";
		}
		return false;
	   }
	   function addToContacts(contactid, username, type) {
		url='/' + username + '/contacts/add/' + contactid
		fetch(url, {
		  method: "POST",
		  headers: {
			"Content-type": "application/json; charset=UTF-8"
		  }
		}).then(response => response.json()).then( response => {
		  iziToast.success({
			title: response.text,
		});
		  document.getElementsByClassName("contacts-count").forEach((contactCount) => {
			contactCount.innerHTML = parseInt(contactCount.innerHTML.trim()) + 1
		  })
		})
		// console.log(document.getElementById(contactid + '-pymk').getElementsByTagName('button')[0].innerHTML)
		if (type == 'pymk') {
		  document.getElementById(contactid + '-pymk').getElementsByTagName('button')[0].innerHTML='Contact Added';
		}
		return false;
	}
	
	function postTextSubmit(event) {
		event.preventDefault()
		form = event.target
		if (form.children[1].value == "") {
		  document.getElementById("emptyformvldtn").classList.remove("hiddenbtn");
		  return false;
		} else {
		  document.getElementById("emptyformvldtn").classList.add("hiddenbtn");
		}
		form.submit()
	  }
	function postSubmit() {
		posttext = document.getElementById("postuploadtext1").value;
		document.getElementById("postuploadtext2").value = posttext;
		document.getElementById("picsubmitbtn").click();
	}
	
	function vidSubmit() {
		posttext = document.getElementById("postuploadtextvid1").value;
		document.getElementById("postuploadtextvid2").value = posttext;
		document.getElementById("vidsubmitbtn").click();
	}
	function updatePhotoUploadText() {
		posttext = document.getElementById("posttextmain").value;
		document.getElementById("postuploadtext1").value = posttext;
	}
	function updateVidUploadText() {
		posttext = document.getElementById("posttextmain").value;
		document.getElementById("postuploadtextvid1").value = posttext;
	}
	
	
	let hiddenPollOptions = 2;
	function unhideOption() {
	  optionToReveal = document.getElementsByClassName("hidden-poll-choice")[0];
	  optionToReveal.classList.remove("hidden-poll-choice");
	  hiddenPollOptions -= 1
	  if (hiddenPollOptions === 0) {
		document.getElementById("addoptionbtn").classList.add("hiddenbtn");
	  }
	}
	function submitVote(pollid, optionid, username) {
	//   console.log("received")
	  url = '/' + username + '/polls/vote/' + optionid
	  fetch(url, {
	  method: "POST",
	  headers: {
		"Content-type": "application/json; charset=UTF-8",
		'X-Requested-With': 'XMLHttpRequest'
	  }
	}).then(response => response.json()).then( responseobj => {
	  for (const key in responseobj) {
		if (key !== 'totalvotes') {
		  document.getElementById(key+'-resultbar').style.width = String(responseobj[key]) + '%'
		  document.getElementById(key+'-resultbar').style["aria-valuenow"] = String(responseobj[key]) + '%'
		  document.getElementById(key+'-result').innerHTML = String(responseobj[key]) + '%'
	
		} else {
		  document.getElementById(pollid+"-totalvotes").innerHTML = String(responseobj[key]) + ' votes'
		}
	  }
	})
		document.getElementById(pollid + '-options').classList.add("hidden-poll-option");
		document.getElementById(pollid + '-results').classList.remove("hidden-poll-option");
	}
	
	
	function displayComments(postid) {
		commentbox = document.getElementById(postid + '-postcomment')
		postcomments = document.getElementById(postid + '-comments')
		loadmorecomments = document.getElementById(postid + '-lmc')
		if (commentbox.classList.contains('hiddencommentsection')) {
			commentbox.classList.remove('hiddencommentsection');
		} else {
			commentbox.classList.add('hiddencommentsection');
		}
	
		if (postcomments.classList.contains('hiddencommentsection')) {
			postcomments.classList.remove('hiddencommentsection');
			loadMoreComments(postid, 1)
		} else {
			postcomments.classList.add('hiddencommentsection');
			postcomments.innerHTML= ""
		}
		if (loadmorecomments.classList.contains('hiddencommentsection') && !postcomments.classList.contains('hiddencommentsection')) {
			loadmorecomments.classList.remove('hiddencommentsection');
		} else {
			loadmorecomments.classList.add('hiddencommentsection');
		}
	}
	function displayReplybox(rbcmtid, ownerUsername) {
		//console.log('called' + rbcmtid)
		if (document.getElementById(rbcmtid + "-comment-replybox") == null) {
			let replyboxtemplate = document.getElementById("replybox-template")
			//commentitem = document.getElementById(commentid + "comment-item")
			let replysection = document.getElementById(rbcmtid + "-comment-replysection")
	// 		console.log(replysection)
			replysection.appendChild(replyboxtemplate.cloneNode(true))
			//console.log(replysection)
			replybox = document.getElementById("replybox-template")
			replyform = document.getElementById("replybox-template-form")
			replyformtext = document.getElementById("replybox-template-formtext")
			replyform.id = rbcmtid + "-reply-formn"
			replybox.id = rbcmtid + "-comment-replybox"
			replyformtext.id = rbcmtid + "-reply-formtext"
			let cmtId = rbcmtid
			replyform.addEventListener("submit", function submitreplywrapper (e) { e.preventDefault()
				return submitReply(e, this, cmtId)})
			replybox.href = "/" + ownerUsername
	
		}
	
		replybox = document.getElementById(rbcmtid + "-comment-replybox")
		if (replybox.classList.contains('hiddencommentsection')) {
			replybox.classList.remove('hiddencommentsection');
		} else {
			replybox.classList.add('hiddencommentsection');
		}
	
	}
	
	function displayReplies(commentid) {
		replies = document.getElementById(commentid + '-comment-replies');
		//loadmorereplies = document.getElementById(commentid + '-lmr');
	
		if (replies.classList.contains('hiddencommentsection')) {
			replies.classList.remove('hiddencommentsection');
			loadMoreReplies(commentid, 1)
		} else {
			replies.classList.add('hiddencommentsection');
			replies.innerHTML= ""
			viewrepliesbtn = document.getElementById(commentid + '-comment-replycount')
			viewrepliesbtn.innerText = 'View ' + viewrepliesbtn.innerText.split(" ")[1] + ' replies'
			if (document.getElementById(commentid+"-lmr") != null) {
				document.getElementById(commentid+"-lmr").classList.add("hiddencommentsection")
			}
		}
	
		//if (loadmorereplies.classList.contains('hiddencommentsection')) {
			//loadmorereplies.classList.remove('hiddencommentsection');
		//} else {
			//loadmorereplies.classList.add('hiddencommentsection');
		//}
	}
	
	
	function submitReply (e, form, cmtId) {
		//console.log(e);
	
		formData = new FormData(form)
		//console.log(formData.get("text"))
		//console.log(formData.get("csrfmiddlewaretoken"))
		//replytext = document.getElementById(rbcmtid + "-reply-formtext").value
		url = '/api/replies/'
		data = {"text":   formData.get("text"), "comment": cmtId}
	// 	console.log(JSON.stringify(data))
			fetch(url, {
				method: "POST",
				headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-Requested-With': 'XMLHttpRequest',
				'X-CSRFToken': formData.get("csrfmiddlewaretoken"),
				},
				body: JSON.stringify(data)
			}).then(response => response.json()).then(response => {
				replies = document.getElementById(cmtId + '-comment-replies');
				if (!replies.classList.contains("hiddencommentsection"))
				{
					displayReplies(cmtId)
				}
				displayReplies(cmtId)
			}).catch(err => { console.error(err) })
	}
	function submitComment (event, postId) {
		event.preventDefault()
		//console.log(e);
		form = event.target
		formData = new FormData(form)
	// 	console.log(formData.get("text"))
	// 	console.log(formData.get("csrfmiddlewaretoken"))
		//replytext = document.getElementById(rbcmtid + "-reply-formtext").value
		url = '/api/comments/'
		data = {"text":   formData.get("text"), "post": postId}
	// 	console.log(JSON.stringify(data))
			fetch(url, {
				method: "POST",
				headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-Requested-With': 'XMLHttpRequest',
				'X-CSRFToken': formData.get("csrfmiddlewaretoken"),
				},
				body: JSON.stringify(data)
			}).then(response => response.json()).then(response => {
				postcomments = document.getElementById(postId + '-comments')
				//postcomments.classList.remove("hiddencommentsection")
				postcomments.innerHTML=""
				loadMoreComments(postId, 1)
			}).catch(err => { console.error(err) })
	}
	
	
	function loadMoreComments(postid, page) {
		if (document.getElementById("comment-template"))
		{
			commenttemplate = document.getElementById("comment-template")
			options = {year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric'};
			url = '/api/comments/?page=' + page +'&postid='+postid
			fetch(url, {
				method: "GET",
				headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-Requested-With': 'XMLHttpRequest',
				},
			}).then(response => response.json()).then(response => {
				postcomments = document.getElementById(postid + "-comments")
				///console.log(postcomments)
				for (result of response.results) {
					//console.log(result.owner.profile.image)
					//commenttemplateclone = commenttemplate.cloneNode()
	
					postcomments.appendChild(commenttemplate.cloneNode(true))
					newcommentitem = document.getElementById("comment-template")
					newcommentitem.id=result.id + "-comment-item"
	
					newcommentimg = document.getElementById("comment-template-img")
					newcommentimg.src = result.owner.profile.image
					newcommentimg.id =result.id + "-comment-img"
					newcommentimg.parentNode.href = '/' + result.owner.username
	
					newcommentownername = document.getElementById("comment-template-ownername");
					newcommentownername.innerText = result.owner.first_name + " " + result.owner.last_name
					newcommentownername.id = result.id + "-comment-ownername"
					newcommentownername.href = "/" + result.owner.username
	
					newcommentcreationdate = document.getElementById("comment-template-creationdate");
					newcommentcreationdate.innerText = new Date(result.created_at).toLocaleDateString("en-US", options)
					newcommentcreationdate.id = result.id + "-comment-creationdate"
	
					newcommenttext = document.getElementById("comment-template-text");
					newcommenttext.innerText = result.text
					newcommenttext.id = result.id + '-comment-text'
					newcommentlikecount = document.getElementById("comment-template-likes");
					newcommentlikecount.innerText = " " + result.like_count
					newcommentlikecount.id = result.id + "comment-likecount"
					if (result.liked) {
						newcommentlikecount.className = "nav-link bi bi-hand-thumbs-up-fill"
					}
					newcommentreplycount = document.getElementById("comment-template-viewreplies");
					newcommentreplycount.innerText = "View " + result.reply_count + " replies"
					newcommentreplycount.id = result.id + '-comment-replycount'
	
					document.getElementById("comment-template-reply").id = result.id + '-comment-reply'
					document.getElementById("comment-template-replies").id = result.id + '-comment-replies'
					document.getElementById("comment-template-replysection").id = result.id + '-comment-replysection'
					let resultId = result.id
					let ownerUsername = result.owner.username
					document.getElementById(result.id + '-comment-reply').addEventListener("click", function drb () {return displayReplybox(resultId, ownerUsername)})
					document.getElementById(result.id + '-comment-replycount').addEventListener("click", function drs () { return displayReplies(resultId)})
					document.getElementById(result.id + "comment-likecount").addEventListener("click", function lco() { return likeCommentObj(resultId, 'comment')})
					newcommentitem.classList.remove("hiddencommentsection")
					//postcomments.getElementById("comment-template").getElementsByTagName("img").src = result.owner.profile.image
					//postcomments.getElementById("comment-template").classList.remove("hiddencommentsection");
	
				}
				page = page + 1
				postitem = document.getElementById(postid + '-item')
				var old_element = document.getElementById(postid+"-lmc-a");
				var new_element = old_element.cloneNode(true);
	// 			console.log(new_element)
				old_element.parentNode.replaceChild(new_element, old_element);
	
				if (response.next != null) {
					//console.log(document.getElementById(postid+"-lmc-a"))
					document.getElementById(postid+"-lmc-a").addEventListener('click', function lmc () { return loadMoreComments(postid, page)})
					document.getElementById(postid+"-lmc").classList.remove("hiddencommentsection")
				} else {
					document.getElementById(postid+"-lmc").classList.add("hiddencommentsection")
				}
				//console.log(document.getElementById(postid+"-lmc-a"))
				//commentsection.getElementsByTagName('img')[0].src = response.results[0].owner.profile.image
			})
		}
	}
	
	function loadMoreReplies(commentid, page) {
		if (document.getElementById("reply-template"))
		{
			replytemplate = document.getElementById("reply-template")
			options = {year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric'};
			url = '/api/replies/?page=' + page +'&commentid='+commentid
			fetch(url, {
				method: "GET",
				headers: {
				"Content-type": "application/json; charset=UTF-8",
				'X-Requested-With': 'XMLHttpRequest',
				},
			}).then(response => response.json()).then(response => {
				commentreplies = document.getElementById(commentid + '-comment-replies')
				///console.log(postcomments)
				for (result of response.results) {
					//console.log(result.owner.profile.image)
					//commenttemplateclone = commenttemplate.cloneNode()
	
					commentreplies.appendChild(replytemplate.cloneNode(true))
					newreplyitem = document.getElementById("reply-template")
					newreplyitem.id=result.id + "-reply-item"
	
					newreplyimg = document.getElementById("reply-template-img")
					newreplyimg.src = result.owner.profile.image
					newreplyimg.id =result.id + "-reply-img"
					newreplyimg.parentNode.href = '/' + result.owner.username
	
					newreplyownername = document.getElementById("reply-template-ownername");
					newreplyownername.innerText = result.owner.first_name + " " + result.owner.last_name
					newreplyownername.id = result.id + "-reply-ownername"
					newreplyownername.href = "/" + result.owner.username
	
					newreplycreationdate = document.getElementById("reply-template-creationdate");
					newreplycreationdate.innerText = new Date(result.created_at).toLocaleDateString("en-US", options)
					newreplycreationdate.id = result.id + "-reply-creationdate"
	
					newreplytext = document.getElementById("reply-template-text");
					newreplytext.innerText = result.text
					newreplytext.id = result.id + '-reply-text'
	
					newreplylikecount = document.getElementById("reply-template-likes");
					newreplylikecount.innerText = " "  + result.like_count
					newreplylikecount.id = result.id + "reply-likecount"
					newreplylikecount.id = result.id + "reply-likecount"
					if (result.liked) {
						newreplylikecount.className = "nav-link bi bi-hand-thumbs-up-fill"
					}
	
					//newcommentreplycount = document.getElementById("comment-template-viewreplies");
					//newcommentreplycount.innerText = "View " + result.reply_count + " replies"
					//newcommentreplycount.id = result.id + '-reply-replycount'
	
					document.getElementById("reply-template-reply").id = result.id + '-reply-reply'
					//document.getElementById("comment-template-replies").id = result.id + '-comment-replies'
					//document.getElementById("comment-template-replysection").id = result.id + '-comment-replysection'
					let commentId = result.comment
					let resultId = result.id
					document.getElementById(result.id + '-reply-reply').addEventListener("click", function drb () {return displayReplybox(commentId)})
					document.getElementById(result.id + "reply-likecount").addEventListener("click", function lro() { return likeCommentObj(resultId, 'reply')})
					//document.getElementById(result.id + '-comment-replycount').addEventListener("click", function drs () { return displayReplies(resultId)})
					newreplyitem.classList.remove("hiddencommentsection")
					//postcomments.getElementById("comment-template").getElementsByTagName("img").src = result.owner.profile.image
					//postcomments.getElementById("comment-template").classList.remove("hiddencommentsection");
	
				}
				viewrepliesbtn = document.getElementById(commentid + '-comment-replycount')
				viewrepliesbtn.innerText = 'Hide '+response.count+' replies'
	
				page = page + 1
				commentitem = document.getElementById(commentid + '-comment-item')
				if (page == 2 && response.next != null) {
					commentitem.appendChild(document.getElementById("comment-template-lmr").cloneNode(true))
					document.getElementById("comment-template-lmr").id = commentid + "-lmr"
				}
				if (page != 2) {
					var old_element = document.getElementById(commentid+"-lmr");
					var new_element = old_element.cloneNode(true);
					old_element.parentNode.replaceChild(new_element, old_element);
				}
	
				if (response.next != null) {
					document.getElementById(commentid+"-lmr").addEventListener('click', function lmc () { return loadMoreReplies(commentid, page)})
					document.getElementById(commentid+"-lmr").classList.remove("hiddencommentsection")
				} else if (page != 2) {
					document.getElementById(commentid+"-lmr").classList.add("hiddencommentsection")
				}
	
				//commentsection.getElementsByTagName('img')[0].src = response.results[0].owner.profile.image
			})
		}
	}
	
	function deletePost(username, postid) {
		token = document.getElementById("replybox-template-form").children[0].value
		url = '/' + String(username)  + '/post/' + String(postid) + '/delete'
		fetch(url, {
			method: "POST",
			headers: {
			"Content-type": "application/json; charset=UTF-8",
			'X-Requested-With': 'XMLHttpRequest',
			'X-CSRFToken': token
			},
			}).then((response) => {
				iziToast.success({
					title: 'Post successfully deleted',
				});
				document.getElementById(postid + "-postobj").remove()
			}).catch((e) => {
				iziToast.error({
					title: 'Error',
					message: 'Something went wrong',
				});
			})
	}
	
	function login(event) {
		event.preventDefault()
		form = event.target
		formData = new FormData(form)
		var data = {};
		formData.forEach((value, key) => data[key] = value);
		url = "/login/"
		fetch(url, {
			method: "POST",
			headers: {
			"Content-type": "application/json; charset=UTF-8",
			'X-Requested-With': 'XMLHttpRequest',
			'X-CSRFToken': formData.get("csrfmiddlewaretoken"),
			},
			body: JSON.stringify(data)
		}).then((response) => {
			if (response.status == 401) {
				iziToast.error({
					title: 'Error',
					message: 'Incorrect login credentials',
				});
			} else if (response.status == 200) {
				iziToast.success({
					title: 'Login Successful',
				});
				window.location.href = '/home'
			} else {
				iziToast.error({
					title: 'Error',
					message: 'Something went wrong',
				});
			}
		})
	}
	
	function userLogin(event) {
		event.preventDefault()
		form = event.target
		formData = new FormData(form)
		var data = {};
		formData.forEach((value, key) => data[key] = value);
		url = "/login/"
		fetch(url, {
			method: "POST",
			headers: {
			"Content-type": "application/json; charset=UTF-8",
			'X-Requested-With': 'XMLHttpRequest',
			'X-CSRFToken': formData.get("csrfmiddlewaretoken"),
			},
			body: JSON.stringify(data)
		}).then((response) => {
			if (response.status == 401) {
				iziToast.error({
					title: 'Error',
					message: 'Incorrect login credentials',
				});
			} else if (response.status == 200) {
				iziToast.success({
					title: 'Login Successful',
				});
				window.location.href = '/home/'
			} else {
				iziToast.error({
					title: 'Error',
					message: 'Something went wrong',
				});
			}
		})
	}
	