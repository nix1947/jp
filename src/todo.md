## TODO: How to setup and call media url.



1. Enable media context processor.
    ```
      'django.template.context_processors.media'
    ```
      

2. Serve media in development mode.

       ```python
      if settings.DEBUG:
       # Serve media in development mode
       urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
      ```
    
3. Call Media path in django template.

   ```html
    <img height="100px" width="100px"src="{{MEDIA_URL}}{{object.logo}}"/>
    ```



## Many to Many table django
To enable 

## Avoid circular imports between class 
Use lazy loading of classes with quotation.
 ```
 user = models.ForeignKey('apps.account.model.UserProfile', related_name='jobs', on_delete=models.SET_NULL, null=True)
    job
 ```

# Get currently rending page full path in template
```python
{{request.get_full_path}}


```