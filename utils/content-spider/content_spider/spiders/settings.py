settings = {
	'el_nacional':{'links':'.md-news-main .bd  .headline a::attr(href)', 'titulo':'.pg-headline strong::text',
	'autor':'.pg-dateline span::text','fecha':'.pg-dateline small::text','body':['.pg-body .mce-body p::text','.pg-body .mce-body p span::text'],'url':'http://www.el-nacional.com/'},
	
	'el_universal':{'links':'article h3 a::attr(href)','titulo':'.title a::text','autor':'meta',
	'fecha':'.dates .clearfix span::text','body':['.note-text p','.note-text div'],'url':'http://www.eluniversal.com/'},
	
	'la_patilla':{'links':'.entry-title a::attr(href)', 'titulo':'header h1::text','autor':'#post-author .profile-content h4::text',
	'fecha':'.post-meta abbr::text','body':'.entry-summary p::text','url':'http://www.lapatilla.com/'},
	
	'dolar_today':{'links':'.post-title a::attr(href)','titulo':'#content h1::text','autor':'#content .meta strong::text',
	'body':'#content p','url':'https://dolartoday.com/'},
	
	'todochavez':{'links':'','titulo':'.texto .titulo::text','autor':'','fecha':'.texto .fecha::text',
	'body':'.contenido p::text','url':'http://www.todochavezenlaweb.gob.ve/ajax/articulos.php?ri=0&rp=400&order=a.fecha&sort=desc&publicado=1&categoria%5B%5D=1'},
	
	'noticias24':{'links':'#mainContent a::attr(href)','titulo':'#singleHeadline h1 a::text','autor':'', 'fecha':['.theMetaTag::text','.theSubExcerpt b'],
	'body':'.theContent p','url':'http://www.noticias24.com/'},
	
	'talcual':{'links':'.usertrue a::attr(href)','titulo':'.notaview header a::text','autor':'.autornota::text', 'fecha':'aside .fechanota::text',
	'body':'.notaview .bodynote p','url':'http://www.talcualdigital.com/'},
	
	'venevision':{'links':'','titulo':'.ArticleDetail h1::text','autor':'', 'fecha':'.ArticleDetail span',
	'body':'.ArticleDetail p','url':'http://noticiero.venevision.net/'},
	
	'globovision':{'links':'http://globovision.com/feed','titulo':'.article-title::text','autor':'.metadata .source', 'fecha':'.metadata .date::text',
	'body':'.article-body p','url':'http://globovision.com/'},
	
	'noticiero_digital':{'links':'#homepage .principal h2 a::attr(href)','titulo':'#contentleft h1::text','autor':'', 'fecha':'.date p::text',
	'body':'#contentleft p','url':'http://www.noticierodigital.com/'},
	
	"la_verdad":{'links':'http://www.laverdad.com/rss/politica','titulo':'header h2::text','autor':'.head .autor::text', 'fecha':'.head .fecha::text',
	'body':'#nota p','url':'http://www.laverdad.com/'},
	
	'informe21':{'links':'.block-inner .item-list h3 a::attr(href)','titulo':'.title::text','autor':'','fecha':'.created::text',
	'body':'.field-item','url':'http://informe21.com/'},
		
	'quinto_dia':{'links':'.page-article .title a::attr(href)','titulo':'.title h1::text','autor':'.texto p strong::text','fecha':'',
	'body':'.texto p','url':'http://www.quintodia.net/'},
	
	'2001':{'links':'.lateral1 td  a::attr(href)','titulo':'.noti_completas .titulo660 h1::text','autor':'','fecha':'.noticia_completa p strong::text',
	'body':'.noticia_completa p','url':'http://www.2001.com.ve/'},
	
	'ultimas_noticias':{'links':'#columna_izq_interna .noticia_rio h2 a::attr(href)','titulo':'#detalle_nota_titulo span::text','autor':'#detalle_nota_redactor span::text',
	'fecha':'#detalle_nota_cab_title::text','body':'#detalle_nota_texto','url':'http://www.ultimasnoticias.com.ve/'},
	
	'noticias_vzla':{'links':'.content .post-title a::attr(href)','titulo':'article .post-title::text','autor':'',
	'fecha':'meta','body':'.entry p','url':'http://noticiasvzla.com/'},
	
	'elcarabobeno':{'links':'.box-title-sm a::attr(href)','titulo':'#articletitle::text','autor':'',
	'fecha':'#articleheader span::text','body':'#articletext','url':'http://www.el-carabobeno.com/'},
	
	'unbombazo':{'links':'.entry-title a::attr(href)','titulo':'.entry-title::text','autor':'',
	'fecha':'div .entry-meta','body':'#content-nt p','url':'http://www.unbombazo.com/'},
	
	'caraota_digital':{'links':'.td-block-span6 a::attr(href)','titulo':'.entry-title::text','autor':'.td-post-author-name a::text',
	'fecha':'.td-post-date time::text','body':'.td-post-content p','url':'http://caraotadigital.net/'},
	}
