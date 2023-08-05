class Config:
    def __init__(
        self,
        container_init_function: callable,
        kernel_class: type,
        root_module_name: str,
        allowed_environments: list,
    ):
        self.__container_init_function = container_init_function
        self.__kernel_class = kernel_class
        self.__root_module_name = root_module_name
        self.__allowed_environments = allowed_environments

    @property
    def container_init_function(self):
        return self.__container_init_function

    @property
    def kernel_class(self):
        return self.__kernel_class

    @property
    def root_module_name(self):
        return self.__root_module_name

    @property
    def allowed_environments(self):
        return self.__allowed_environments
