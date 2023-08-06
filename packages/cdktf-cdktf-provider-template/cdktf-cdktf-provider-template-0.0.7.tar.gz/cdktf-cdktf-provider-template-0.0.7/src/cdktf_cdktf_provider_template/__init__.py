'''
# Terraform CDK template Provider ~> 2.2

This repo builds and publishes the Terraform template Provider bindings for [cdktf](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-template](https://www.npmjs.com/package/@cdktf/provider-template).

`npm install @cdktf/provider-template`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-template](https://pypi.org/project/cdktf-cdktf-provider-template).

`pipenv install cdktf-cdktf-provider-template`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Template](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Template).

`dotnet add package HashiCorp.Cdktf.Providers.Template`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-template](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-template).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-template</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

## Docs

Find auto-generated docs for this provider here: [./API.md](./API.md)

## Versioning

This project is explicitly not tracking the Terraform template Provider version 1:1. In fact, it always tracks `latest` of `~> 2.2` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform template Provider](https://github.com/terraform-providers/terraform-provider-template)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped. While the Terraform Engine and the Terraform template Provider are relatively stable, the Terraform CDK is in an early stage. Therefore, it's likely that there will be breaking changes.

## Features / Issues / Bugs

Please report bugs and issues to the [terraform cdk](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### projen

This is mostly based on [projen](https://github.com/eladb/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on projen

There's a custom [project builder](https://github.com/hashicorp/cdktf-provider-project) which encapsulate the common settings for all `cdktf` providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [Repository Manager](https://github.com/hashicorp/cdktf-repository-manager/)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import cdktf
import constructs


class CloudinitConfig(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-template.CloudinitConfig",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config template_cloudinit_config}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        part: typing.Union[cdktf.IResolvable, typing.Sequence["CloudinitConfigPart"]],
        base64_encode: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        gzip: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config template_cloudinit_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param part: part block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#part CloudinitConfig#part}
        :param base64_encode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#base64_encode CloudinitConfig#base64_encode}.
        :param gzip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#gzip CloudinitConfig#gzip}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#id CloudinitConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = CloudinitConfigConfig(
            part=part,
            base64_encode=base64_encode,
            gzip=gzip,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPart")
    def put_part(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence["CloudinitConfigPart"]],
    ) -> None:
        '''
        :param value: -
        '''
        return typing.cast(None, jsii.invoke(self, "putPart", [value]))

    @jsii.member(jsii_name="resetBase64Encode")
    def reset_base64_encode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBase64Encode", []))

    @jsii.member(jsii_name="resetGzip")
    def reset_gzip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGzip", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="part")
    def part(self) -> "CloudinitConfigPartList":
        return typing.cast("CloudinitConfigPartList", jsii.get(self, "part"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rendered")
    def rendered(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rendered"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="base64EncodeInput")
    def base64_encode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "base64EncodeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="gzipInput")
    def gzip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "gzipInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="partInput")
    def part_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CloudinitConfigPart"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["CloudinitConfigPart"]]], jsii.get(self, "partInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="base64Encode")
    def base64_encode(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "base64Encode"))

    @base64_encode.setter
    def base64_encode(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "base64Encode", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="gzip")
    def gzip(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "gzip"))

    @gzip.setter
    def gzip(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "gzip", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-template.CloudinitConfigConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "part": "part",
        "base64_encode": "base64Encode",
        "gzip": "gzip",
        "id": "id",
    },
)
class CloudinitConfigConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        part: typing.Union[cdktf.IResolvable, typing.Sequence["CloudinitConfigPart"]],
        base64_encode: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        gzip: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param part: part block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#part CloudinitConfig#part}
        :param base64_encode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#base64_encode CloudinitConfig#base64_encode}.
        :param gzip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#gzip CloudinitConfig#gzip}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#id CloudinitConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "part": part,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if base64_encode is not None:
            self._values["base64_encode"] = base64_encode
        if gzip is not None:
            self._values["gzip"] = gzip
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def part(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["CloudinitConfigPart"]]:
        '''part block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#part CloudinitConfig#part}
        '''
        result = self._values.get("part")
        assert result is not None, "Required property 'part' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["CloudinitConfigPart"]], result)

    @builtins.property
    def base64_encode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#base64_encode CloudinitConfig#base64_encode}.'''
        result = self._values.get("base64_encode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def gzip(self) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#gzip CloudinitConfig#gzip}.'''
        result = self._values.get("gzip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#id CloudinitConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudinitConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-template.CloudinitConfigPart",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "content_type": "contentType",
        "filename": "filename",
        "merge_type": "mergeType",
    },
)
class CloudinitConfigPart:
    def __init__(
        self,
        *,
        content: builtins.str,
        content_type: typing.Optional[builtins.str] = None,
        filename: typing.Optional[builtins.str] = None,
        merge_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#content CloudinitConfig#content}.
        :param content_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#content_type CloudinitConfig#content_type}.
        :param filename: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#filename CloudinitConfig#filename}.
        :param merge_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#merge_type CloudinitConfig#merge_type}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "content": content,
        }
        if content_type is not None:
            self._values["content_type"] = content_type
        if filename is not None:
            self._values["filename"] = filename
        if merge_type is not None:
            self._values["merge_type"] = merge_type

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#content CloudinitConfig#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#content_type CloudinitConfig#content_type}.'''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#filename CloudinitConfig#filename}.'''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/cloudinit_config#merge_type CloudinitConfig#merge_type}.'''
        result = self._values.get("merge_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudinitConfigPart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudinitConfigPartList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-template.CloudinitConfigPartList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CloudinitConfigPartOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        return typing.cast("CloudinitConfigPartOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        jsii.set(self, "terraformResource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        jsii.set(self, "wrapsSet", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CloudinitConfigPart]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CloudinitConfigPart]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[CloudinitConfigPart]]],
    ) -> None:
        jsii.set(self, "internalValue", value)


class CloudinitConfigPartOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-template.CloudinitConfigPartOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @jsii.member(jsii_name="resetMergeType")
    def reset_merge_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeType", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mergeTypeInput")
    def merge_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeTypeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        jsii.set(self, "content", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        jsii.set(self, "contentType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        jsii.set(self, "filename", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mergeType")
    def merge_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeType"))

    @merge_type.setter
    def merge_type(self, value: builtins.str) -> None:
        jsii.set(self, "mergeType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, CloudinitConfigPart]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, CloudinitConfigPart]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, CloudinitConfigPart]],
    ) -> None:
        jsii.set(self, "internalValue", value)


class DataTemplateCloudinitConfig(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-template.DataTemplateCloudinitConfig",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config template_cloudinit_config}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        part: typing.Union[cdktf.IResolvable, typing.Sequence["DataTemplateCloudinitConfigPart"]],
        base64_encode: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        gzip: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config template_cloudinit_config} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param part: part block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#part DataTemplateCloudinitConfig#part}
        :param base64_encode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#base64_encode DataTemplateCloudinitConfig#base64_encode}.
        :param gzip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#gzip DataTemplateCloudinitConfig#gzip}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#id DataTemplateCloudinitConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTemplateCloudinitConfigConfig(
            part=part,
            base64_encode=base64_encode,
            gzip=gzip,
            id=id,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPart")
    def put_part(
        self,
        value: typing.Union[cdktf.IResolvable, typing.Sequence["DataTemplateCloudinitConfigPart"]],
    ) -> None:
        '''
        :param value: -
        '''
        return typing.cast(None, jsii.invoke(self, "putPart", [value]))

    @jsii.member(jsii_name="resetBase64Encode")
    def reset_base64_encode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBase64Encode", []))

    @jsii.member(jsii_name="resetGzip")
    def reset_gzip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGzip", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="part")
    def part(self) -> "DataTemplateCloudinitConfigPartList":
        return typing.cast("DataTemplateCloudinitConfigPartList", jsii.get(self, "part"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rendered")
    def rendered(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rendered"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="base64EncodeInput")
    def base64_encode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "base64EncodeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="gzipInput")
    def gzip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], jsii.get(self, "gzipInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="partInput")
    def part_input(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List["DataTemplateCloudinitConfigPart"]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List["DataTemplateCloudinitConfigPart"]]], jsii.get(self, "partInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="base64Encode")
    def base64_encode(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "base64Encode"))

    @base64_encode.setter
    def base64_encode(
        self,
        value: typing.Union[builtins.bool, cdktf.IResolvable],
    ) -> None:
        jsii.set(self, "base64Encode", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="gzip")
    def gzip(self) -> typing.Union[builtins.bool, cdktf.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, cdktf.IResolvable], jsii.get(self, "gzip"))

    @gzip.setter
    def gzip(self, value: typing.Union[builtins.bool, cdktf.IResolvable]) -> None:
        jsii.set(self, "gzip", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-template.DataTemplateCloudinitConfigConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "part": "part",
        "base64_encode": "base64Encode",
        "gzip": "gzip",
        "id": "id",
    },
)
class DataTemplateCloudinitConfigConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        part: typing.Union[cdktf.IResolvable, typing.Sequence["DataTemplateCloudinitConfigPart"]],
        base64_encode: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        gzip: typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param part: part block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#part DataTemplateCloudinitConfig#part}
        :param base64_encode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#base64_encode DataTemplateCloudinitConfig#base64_encode}.
        :param gzip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#gzip DataTemplateCloudinitConfig#gzip}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#id DataTemplateCloudinitConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "part": part,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if base64_encode is not None:
            self._values["base64_encode"] = base64_encode
        if gzip is not None:
            self._values["gzip"] = gzip
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def part(
        self,
    ) -> typing.Union[cdktf.IResolvable, typing.List["DataTemplateCloudinitConfigPart"]]:
        '''part block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#part DataTemplateCloudinitConfig#part}
        '''
        result = self._values.get("part")
        assert result is not None, "Required property 'part' is missing"
        return typing.cast(typing.Union[cdktf.IResolvable, typing.List["DataTemplateCloudinitConfigPart"]], result)

    @builtins.property
    def base64_encode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#base64_encode DataTemplateCloudinitConfig#base64_encode}.'''
        result = self._values.get("base64_encode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def gzip(self) -> typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#gzip DataTemplateCloudinitConfig#gzip}.'''
        result = self._values.get("gzip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, cdktf.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#id DataTemplateCloudinitConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTemplateCloudinitConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-template.DataTemplateCloudinitConfigPart",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "content_type": "contentType",
        "filename": "filename",
        "merge_type": "mergeType",
    },
)
class DataTemplateCloudinitConfigPart:
    def __init__(
        self,
        *,
        content: builtins.str,
        content_type: typing.Optional[builtins.str] = None,
        filename: typing.Optional[builtins.str] = None,
        merge_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#content DataTemplateCloudinitConfig#content}.
        :param content_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#content_type DataTemplateCloudinitConfig#content_type}.
        :param filename: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#filename DataTemplateCloudinitConfig#filename}.
        :param merge_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#merge_type DataTemplateCloudinitConfig#merge_type}.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "content": content,
        }
        if content_type is not None:
            self._values["content_type"] = content_type
        if filename is not None:
            self._values["filename"] = filename
        if merge_type is not None:
            self._values["merge_type"] = merge_type

    @builtins.property
    def content(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#content DataTemplateCloudinitConfig#content}.'''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#content_type DataTemplateCloudinitConfig#content_type}.'''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#filename DataTemplateCloudinitConfig#filename}.'''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/cloudinit_config#merge_type DataTemplateCloudinitConfig#merge_type}.'''
        result = self._values.get("merge_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTemplateCloudinitConfigPart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTemplateCloudinitConfigPartList(
    cdktf.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-template.DataTemplateCloudinitConfigPartList",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataTemplateCloudinitConfigPartOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        return typing.cast("DataTemplateCloudinitConfigPartOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> cdktf.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(cdktf.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: cdktf.IInterpolatingParent) -> None:
        jsii.set(self, "terraformResource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        jsii.set(self, "wrapsSet", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DataTemplateCloudinitConfigPart]]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DataTemplateCloudinitConfigPart]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, typing.List[DataTemplateCloudinitConfigPart]]],
    ) -> None:
        jsii.set(self, "internalValue", value)


class DataTemplateCloudinitConfigPartOutputReference(
    cdktf.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-template.DataTemplateCloudinitConfigPartOutputReference",
):
    def __init__(
        self,
        terraform_resource: cdktf.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContentType")
    def reset_content_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentType", []))

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @jsii.member(jsii_name="resetMergeType")
    def reset_merge_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMergeType", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="contentTypeInput")
    def content_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentTypeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mergeTypeInput")
    def merge_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mergeTypeInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        jsii.set(self, "content", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        jsii.set(self, "contentType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        jsii.set(self, "filename", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="mergeType")
    def merge_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mergeType"))

    @merge_type.setter
    def merge_type(self, value: builtins.str) -> None:
        jsii.set(self, "mergeType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[cdktf.IResolvable, DataTemplateCloudinitConfigPart]]:
        return typing.cast(typing.Optional[typing.Union[cdktf.IResolvable, DataTemplateCloudinitConfigPart]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[cdktf.IResolvable, DataTemplateCloudinitConfigPart]],
    ) -> None:
        jsii.set(self, "internalValue", value)


class DataTemplateFile(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-template.DataTemplateFile",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/template/d/file template_file}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        filename: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
        vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/template/d/file template_file} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filename: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#filename DataTemplateFile#filename}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#id DataTemplateFile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param template: Contents of the template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#template DataTemplateFile#template}
        :param vars: variables to substitute. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#vars DataTemplateFile#vars}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataTemplateFileConfig(
            filename=filename,
            id=id,
            template=template,
            vars=vars,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTemplate")
    def reset_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplate", []))

    @jsii.member(jsii_name="resetVars")
    def reset_vars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVars", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rendered")
    def rendered(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rendered"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="varsInput")
    def vars_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "varsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        jsii.set(self, "filename", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        jsii.set(self, "template", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vars")
    def vars(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "vars"))

    @vars.setter
    def vars(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        jsii.set(self, "vars", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-template.DataTemplateFileConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "filename": "filename",
        "id": "id",
        "template": "template",
        "vars": "vars",
    },
)
class DataTemplateFileConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        filename: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
        vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param filename: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#filename DataTemplateFile#filename}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#id DataTemplateFile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param template: Contents of the template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#template DataTemplateFile#template}
        :param vars: variables to substitute. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#vars DataTemplateFile#vars}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if filename is not None:
            self._values["filename"] = filename
        if id is not None:
            self._values["id"] = id
        if template is not None:
            self._values["template"] = template
        if vars is not None:
            self._values["vars"] = vars

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#filename DataTemplateFile#filename}.'''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#id DataTemplateFile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''Contents of the template.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#template DataTemplateFile#template}
        '''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vars(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''variables to substitute.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/d/file#vars DataTemplateFile#vars}
        '''
        result = self._values.get("vars")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTemplateFileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Dir(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-template.Dir",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/template/r/dir template_dir}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        destination_dir: builtins.str,
        source_dir: builtins.str,
        id: typing.Optional[builtins.str] = None,
        vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/template/r/dir template_dir} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination_dir: Path to the directory where the templated files will be written. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#destination_dir Dir#destination_dir}
        :param source_dir: Path to the directory where the files to template reside. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#source_dir Dir#source_dir}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#id Dir#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param vars: Variables to substitute. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#vars Dir#vars}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DirConfig(
            destination_dir=destination_dir,
            source_dir=source_dir,
            id=id,
            vars=vars,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetVars")
    def reset_vars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVars", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="destinationDirInput")
    def destination_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationDirInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourceDirInput")
    def source_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDirInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="varsInput")
    def vars_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "varsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="destinationDir")
    def destination_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationDir"))

    @destination_dir.setter
    def destination_dir(self, value: builtins.str) -> None:
        jsii.set(self, "destinationDir", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourceDir")
    def source_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDir"))

    @source_dir.setter
    def source_dir(self, value: builtins.str) -> None:
        jsii.set(self, "sourceDir", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vars")
    def vars(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "vars"))

    @vars.setter
    def vars(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        jsii.set(self, "vars", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-template.DirConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "destination_dir": "destinationDir",
        "source_dir": "sourceDir",
        "id": "id",
        "vars": "vars",
    },
)
class DirConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        destination_dir: builtins.str,
        source_dir: builtins.str,
        id: typing.Optional[builtins.str] = None,
        vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param destination_dir: Path to the directory where the templated files will be written. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#destination_dir Dir#destination_dir}
        :param source_dir: Path to the directory where the files to template reside. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#source_dir Dir#source_dir}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#id Dir#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param vars: Variables to substitute. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#vars Dir#vars}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "destination_dir": destination_dir,
            "source_dir": source_dir,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if id is not None:
            self._values["id"] = id
        if vars is not None:
            self._values["vars"] = vars

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def destination_dir(self) -> builtins.str:
        '''Path to the directory where the templated files will be written.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#destination_dir Dir#destination_dir}
        '''
        result = self._values.get("destination_dir")
        assert result is not None, "Required property 'destination_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_dir(self) -> builtins.str:
        '''Path to the directory where the files to template reside.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#source_dir Dir#source_dir}
        '''
        result = self._values.get("source_dir")
        assert result is not None, "Required property 'source_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#id Dir#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vars(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Variables to substitute.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/dir#vars Dir#vars}
        '''
        result = self._values.get("vars")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DirConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class File(
    cdktf.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-template.File",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/template/r/file template_file}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id_: builtins.str,
        *,
        filename: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
        vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/template/r/file template_file} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filename: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#filename File#filename}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#id File#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param template: Contents of the template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#template File#template}
        :param vars: variables to substitute. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#vars File#vars}
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = FileConfig(
            filename=filename,
            id=id,
            template=template,
            vars=vars,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetFilename")
    def reset_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilename", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTemplate")
    def reset_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplate", []))

    @jsii.member(jsii_name="resetVars")
    def reset_vars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVars", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rendered")
    def rendered(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rendered"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="varsInput")
    def vars_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "varsInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        jsii.set(self, "filename", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        jsii.set(self, "template", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vars")
    def vars(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "vars"))

    @vars.setter
    def vars(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        jsii.set(self, "vars", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-template.FileConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "filename": "filename",
        "id": "id",
        "template": "template",
        "vars": "vars",
    },
)
class FileConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        filename: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
        vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param filename: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#filename File#filename}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#id File#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param template: Contents of the template. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#template File#template}
        :param vars: variables to substitute. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#vars File#vars}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if filename is not None:
            self._values["filename"] = filename
        if id is not None:
            self._values["id"] = id
        if template is not None:
            self._values["template"] = template
        if vars is not None:
            self._values["vars"] = vars

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def filename(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#filename File#filename}.'''
        result = self._values.get("filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#id File#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''Contents of the template.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#template File#template}
        '''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vars(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''variables to substitute.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template/r/file#vars File#vars}
        '''
        result = self._values.get("vars")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TemplateProvider(
    cdktf.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-template.TemplateProvider",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/template template}.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/template template} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template#alias TemplateProvider#alias}
        '''
        config = TemplateProviderConfig(alias=alias)

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "alias", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-template.TemplateProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"alias": "alias"},
)
class TemplateProviderConfig:
    def __init__(self, *, alias: typing.Optional[builtins.str] = None) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template#alias TemplateProvider#alias}
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/template#alias TemplateProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TemplateProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudinitConfig",
    "CloudinitConfigConfig",
    "CloudinitConfigPart",
    "CloudinitConfigPartList",
    "CloudinitConfigPartOutputReference",
    "DataTemplateCloudinitConfig",
    "DataTemplateCloudinitConfigConfig",
    "DataTemplateCloudinitConfigPart",
    "DataTemplateCloudinitConfigPartList",
    "DataTemplateCloudinitConfigPartOutputReference",
    "DataTemplateFile",
    "DataTemplateFileConfig",
    "Dir",
    "DirConfig",
    "File",
    "FileConfig",
    "TemplateProvider",
    "TemplateProviderConfig",
]

publication.publish()
